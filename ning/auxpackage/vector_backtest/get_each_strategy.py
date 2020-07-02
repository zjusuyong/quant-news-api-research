# -*- coding: UTF-8 -*-
from auxpackage.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
from auxpackage import quant_package as qp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

register_matplotlib_converters()


class FeedBack:
    def __init__(self, df, l_each_close_pct, l_signal, l_cum_strategy_pct, rf=0.028, year_tradeday=250):
        """
        输出回测统计
        :param df:
        :param l_each_close_pct: list, 每一Kline的pct_change
        :param l_signal: DataFrame.Series, bool信号Series
        :param l_cum_strategy_pct: DataFrame.Series, 累计收益率Series
        :param rf: 无风险利率, default: 0.028
        """
        self.df = df
        self.l_each_close_pct = l_each_close_pct
        self.l_signal = np.array(l_signal)
        self.l_cum_strategy_pct = l_cum_strategy_pct
        self.rf = rf
        self.year_tradeday = year_tradeday
        self.kline_num = len(self.l_signal)
        self.l_cum_benchmark_pct = (1 + self.l_each_close_pct).cumprod()

        self.l_holdidx = None

        self.l_each_strategy_pct = None
        self.avg_strategy_pct = None
        self.profit_num = None
        self.profit_avg_pct = None
        self.loss_num = None
        self.loss_avg_pct = None
        self.win_pct = None
        self.winloss_pct = None

        self.strategy_pct = None
        self.strategy_ytd_pct = None
        self.benchmark_pct = None
        self.benchmark_ytd_pct = None
        self.car_pct = None
        self.max_each_strategy_pct = None
        self.min_each_strategy_pct = None

        self.l_each_holdtime = None
        self.avg_holdtime = None
        self.profit_avg_holdtime = None
        self.loss_avg_holdtime = None

        self.mdd_pct = None
        self.mdd_range = None
        self.mrg_pct = None
        self.mrg_range = None

        self.tradeday_num = None
        self.tradeday_pct = None

        self.sharpe_pct = None
        self.info_pct = None
        self.benchmark_volatility = None
        self.strategy_volatility = None

        self.sharpe_pct = None
        self.info_pct = None
        self.benchmark_volatility = None
        self.strategy_volatility = None
        self.bate = None
        self.alpha = None

    def get_holdidx(self):
        """
        获取持仓索引列表l_holdidx
            l_aux eg: [1, 3, 4, 6, 7, 8], 两两一组，表示开仓和平仓的索引，第一笔交易开仓1，平仓3，第二笔交易开仓4，平仓6...
            l_holdidx: [[4, 6], [8, 20], [45, 47]], 每一个元素表示一次交易，内层列表表示每一次交易开始和结束的索引
        process：
            l_signal是信号布尔列表->aux，1表示满足开仓条件，持有仓位，0表示不满足开仓条件，没有仓位
            l_signal平移一位相减，得到的列表只包括1/0/-1三种情况，1为开仓，-1为平仓，
            存在一种特殊情况，最后一次开仓后，在测试数据范围内没有满足平仓条件，需要判断后补上一个-1表示平仓
            信号布尔列表aux只保留1和-1值后，得到的就是开平仓的列表，取其索引得到l_aux
            通过l_aux获取到l_holdidx
        :return:
        """
        ap.sound(f'entry: get_holdidx')

        df_temp = pd.DataFrame()
        df_temp['sig'] = self.l_signal
        df_temp['sig_shift'] = self.l_signal
        df_temp['sig_shift'] = df_temp['sig_shift'].shift(1).fillna(0).astype(int)
        df_temp['aux'] = df_temp['sig'] - df_temp['sig_shift']
        df_temp = df_temp.reset_index()
        df_aux = df_temp[['aux']][df_temp['aux'] != 0].reset_index().copy()

        if df_aux.loc[len(df_aux) - 1, 'aux'] == 1:
            df_aux = ap.concat(df_aux,
                               pd.DataFrame({'index': [df_aux['index'].tolist()[-1] + 1], 'aux': [-1]}))
        l_aux = df_aux['index'].tolist()
        step = 2
        self.l_holdidx = [l_aux[i:i + step] for i in range(0, len(l_aux), step)]

        print(f'df_aux: {df_aux.head()}')
        return self

    def stat_yield(self):
        """
        统计收益率相关指标:
            l_each_strategy_pct: 每一笔交易的收益率
            avg_strategy_pct: 总体平均收益率
            profit_num: 盈利交易次数
            profit_avg_pct: 盈利交易平均收益率
            loss_num: 亏损交易次数
            loss_avg_pct: 亏损交易平均收益率
            win_pct: 胜率
            winloss_pct: 盈亏比
            strategy_pct: 策略总收益率
            strategy_ytd_pct: 策略年化收益率
            benchmark_pct: 基准总收益率
            benchmark_ytd_pct: 基准年化收益率
            car_pct: 超额收益率
            max_each_strategy_pct: 策略单笔交易最大收益率
            min_each_strategy_pct: 策略单笔交易最小收益率
        :return:
        """
        ap.sound(f'entry: stat_strategy')
        self.l_each_strategy_pct = [sum(self.l_each_close_pct[x:y]) for (x, y) in self.l_holdidx]
        self.avg_strategy_pct = float(np.mean(self.l_each_strategy_pct))

        self.profit_num = len([i for i in self.l_each_strategy_pct if i > 0])
        self.profit_avg_pct = float(np.mean([i for i in self.l_each_strategy_pct if i > 0]))
        self.loss_num = len([i for i in self.l_each_strategy_pct if i <= 0])
        self.loss_avg_pct = float(np.mean([i for i in self.l_each_strategy_pct if i <= 0]))
        self.win_pct = self.profit_num / (self.profit_num + self.loss_num)
        self.winloss_pct = sum([i for i in self.l_each_strategy_pct if i > 0]) / sum(
            [i for i in self.l_each_strategy_pct if i <= 0])

        self.strategy_pct = (self.l_cum_strategy_pct[-1] - 1)
        self.strategy_ytd_pct = qp.total_annualized_returns(self.strategy_pct, self.year_tradeday, self.kline_num)

        self.benchmark_pct = (self.df['close'][-1] - self.df['close'][0]) / self.df['close'][0]
        self.benchmark_ytd_pct = self.benchmark_pct / self.kline_num * self.year_tradeday

        self.car_pct = self.strategy_ytd_pct - self.benchmark_ytd_pct

        self.max_each_strategy_pct = max(self.l_cum_strategy_pct[1:])
        self.min_each_strategy_pct = min(self.l_cum_strategy_pct[1:])

        return self

    def stat_holdtime(self):
        """
        统计持仓时间相关指标:
            l_each_holdtime: 每一笔交易持仓时间
            avg_holdtime: 总平均持仓时间
            profit_avg_holdtime: 盈利交易平均持仓时间
            loss_avg_holdtime: 亏损交易平均持仓时间
        :return:
        """
        ap.sound(f'entry: stat_holdtime')

        self.l_each_holdtime = [y - x for (x, y) in self.l_holdidx]
        self.avg_holdtime = np.mean(self.l_each_holdtime)

        arr_each_strategy = np.array(self.l_each_strategy_pct)
        arr_each_holdtime = np.array(self.l_each_holdtime)
        arr_profit = arr_each_holdtime[arr_each_strategy > 0]
        arr_loss = arr_each_holdtime[arr_each_strategy <= 0]
        self.profit_avg_holdtime = np.mean(arr_profit)
        self.loss_avg_holdtime = np.mean(arr_loss)
        return self

    def stat_maxtrade(self):
        """
        统计最大回撤交易和最大增长交易
            mdd_pct: 最大回撤比率
            mdd_range: 最大回撤所在序列范围
            mrg_pct: 最大增长比率
            mrg_range: 最大增长所在序列范围
        :return:
        """
        ap.sound(f'entry: stat_maxtrade')
        mdd = qp.maxdrawdown(np.array(self.l_cum_strategy_pct[1:]))
        self.mdd_pct = mdd['pct']
        self.mdd_range = mdd['range']

        mrg = qp.maxrevenuegrowth(np.array(self.l_cum_strategy_pct[1:]))
        self.mrg_pct = mrg['pct']
        self.mrg_range = mrg['range']
        return self

    def stat_tradeday(self):
        """
        统计交易日相关指标:
            tradeday_num: 交易日总数
            tradeday_pct: 交易日占比
        :return:
        """
        ap.sound(f'entry: stat_tradeday')
        self.tradeday_num = len([i for i in self.l_signal if i == 1])
        self.tradeday_pct = self.tradeday_num / self.kline_num
        return self

    def stat_otherindex(self):
        """
        计算其他指标:
            sharpe_pct: 夏普比率
            info_pct: 信息比率
            benchmark_volatility: 基准波动率
            strategy_volatility: 策略波动率
            bate: 贝塔值
            alpha: 阿尔法值
        :return:
        """
        ap.sound(f'entry: stat_shape')

        self.sharpe_pct = qp.sharpe_ratio(self.strategy_ytd_pct, self.l_cum_strategy_pct, self.rf)
        self.info_pct = qp.information_ratio(self.l_each_strategy_pct, self.l_each_close_pct,
                                             self.strategy_ytd_pct, self.benchmark_ytd_pct, self.year_tradeday)
        self.benchmark_volatility = qp.volatility(self.l_each_close_pct, self.year_tradeday, self.kline_num)
        self.strategy_volatility = qp.volatility(self.l_each_strategy_pct, self.year_tradeday, self.kline_num)
        self.bate = qp.bate(self.l_each_strategy_pct, self.l_each_close_pct)
        self.alpha = qp.alpha(self.strategy_ytd_pct, self.benchmark_ytd_pct, self.rf, self.bate)

        return self

    def output(self):
        ap.sound(f'entry: output')
        print(f'基准总收益率: {round(self.benchmark_pct, 4)}, 策略总收益率: {round(self.strategy_pct, 4)}\n'
              f'基准年化收益率: {round(self.benchmark_ytd_pct, 4)}, 策略年化收益率: {round(self.strategy_ytd_pct, 4)}\n'
              f'超额收益率: {round(self.car_pct, 4)}, 胜率: {round(self.win_pct, 4)}, 盈亏比: {round(self.winloss_pct, 4)}\n'
              f'夏普比率: {round(self.sharpe_pct, 4)}, Alpha: {round(self.alpha, 4)}, Bate: {round(self.bate, 4)}\n'
              f'信息比率: {round(self.info_pct, 4)}, 策略波动率: {round(self.strategy_volatility, 4)}, '
              f'基准波动率: {round(self.benchmark_volatility, 4)}'
              f'最高浮动收益率: {round(self.max_each_strategy_pct, 4)}, '
              f'最低浮动收益率: {round(self.min_each_strategy_pct, 4)}\n'
              f'最大回撤率: {round(self.mdd_pct, 4)}, 最大回撤位置: {self.mdd_range}\n'
              f'最大收益率: {round(self.mrg_pct, 4)}, 最大收益位置: {self.mrg_range}\n'
              f'总交易次数: {len(self.l_each_strategy_pct)}, 平均收益率: {round(self.avg_strategy_pct, 4)}, '
              f'平均持仓时间: {self.avg_holdtime}\n'
              f'盈利交易次数: {self.profit_num}, 盈利交易平均收益率: {round(self.profit_avg_pct, 4)}, '
              f'盈利交易平均持仓时间: {self.profit_avg_holdtime}\n'
              f'亏损交易次数: {self.loss_num}, 亏损交易平均收益率: {round(self.loss_avg_pct, 4)}, '
              f'亏损交易平均持仓时间: {self.loss_avg_holdtime}\n'
              f'总测试天数: {self.kline_num}, 持仓天数: {self.tradeday_num}, 持仓天数占比: {round(self.tradeday_pct, 2)}')

        return self

    def draw(self):
        ap.sound(f'entry: draw')
        df = pd.DataFrame()
        df['holdtime'] = self.l_each_holdtime
        df['strategy'] = self.l_each_strategy_pct
        with sns.axes_style("dark"):
            sns.jointplot('holdtime', 'strategy', data=df,
                          kind='kde', color='grey', space=0, pct=6)
        plt.show()
        return self

    def run(self):
        self.get_holdidx()
        self.stat_yield()
        self.stat_holdtime()
        self.stat_maxtrade()
        self.stat_tradeday()
        self.stat_otherindex()
        self.output()
        self.draw()
        return self
