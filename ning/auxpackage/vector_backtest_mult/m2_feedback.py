# -*- coding: UTF-8 -*-
from auxpackage.tookit.analysis_package import ap
from auxpackage.tookit import quant_package as qp
import numpy as np


class FeedBack:
    def __init__(self, df, l_signal, l_long_signal, l_short_signal, l_each_benchmark_pct, l_each_strategy_pct,
                 l_cum_strategy_pct, rf=0.028,
                 year_tradeday=250):
        """
        输出回测统计
        :param df:
        :param l_signal: DataFrame.Series, bool信号Series
        :param l_long_signal: DataFrame.Series, bool信号Series
        :param l_short_signal: DataFrame.Series, bool信号Series
        :param l_each_benchmark_pct: list, 每一Kline的pct_change
        :param l_each_strategy_pct: list, 每一Kline的策略收益
        :param l_cum_strategy_pct: DataFrame.Series, 累计收益率Series
        :param rf: 无风险利率, default: 0.028
        """
        self.df = df
        self.l_signal = np.array(l_signal)
        self.l_long_signal = np.array(l_long_signal)
        self.l_short_signal = np.array(l_short_signal)

        self.l_each_benchmark_pct = np.array(l_each_benchmark_pct)
        self.l_each_strategy_pct = np.array(l_each_strategy_pct)
        self.l_cum_strategy_pct = np.array(l_cum_strategy_pct)
        self.rf = rf
        self.year_tradeday = year_tradeday
        self.kline_num = len(self.l_each_benchmark_pct)

        self.l_close = self.df['close'].tolist()
        self.l_long_holdidx = None
        self.l_short_holdidx = None
        self.l_holdidx = None

        self.l_stroke_pct = None
        self.l_long_stroke_pct = None
        self.l_short_stroke_pct = None
        self.avg_stroke_pct = None
        self.profit_num = None
        self.profit_avg_pct = None
        self.loss_num = None
        self.loss_avg_pct = None
        self.win_pct = None
        self.winloss_pct = None

        self.strategy_total_pct = None
        self.strategy_ytd_pct = None
        self.benchmark_total_pct = None
        self.benchmark_ytd_pct = None
        self.car_pct = None
        self.max_each_strategy_pct = None
        self.min_each_strategy_pct = None

        self.l_stroke_holdtime = None
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

    def get_stroke_pct(self):
        """
        计算每笔交易收益率
        :return:
        """
        ap.sound(f'entry: get_holdidx')
        # todo: 这里发现开始并不只是1，也有12等，结束不只是-11，也有-12等，需要用别的办法处理
        self.l_long_holdidx = qp.get_holdidx(self.l_long_signal)
        self.l_short_holdidx = qp.get_holdidx(self.l_short_signal)
        self.l_holdidx = qp.get_holdidx(self.l_signal)

        self.l_long_stroke_pct = [sum(self.l_each_benchmark_pct[x:y]) for (x, y) in self.l_long_holdidx]
        self.l_short_stroke_pct = [-1 * sum(self.l_each_benchmark_pct[x:y]) for (x, y) in self.l_short_holdidx]

        self.l_stroke_pct = self.l_long_stroke_pct + self.l_short_stroke_pct
        return self

    def stat_yield(self):
        """
        统计收益率相关指标:
            l_stroke_pct: 每一笔交易的收益率
            avg_stroke_pct: 总体平均收益率
            profit_num: 盈利交易次数
            profit_avg_pct: 盈利交易平均收益率
            loss_num: 亏损交易次数
            loss_avg_pct: 亏损交易平均收益率
            win_pct: 胜率
            winloss_pct: 盈亏比
            strategy_total_pct: 策略总收益率
            strategy_ytd_pct: 策略年化收益率
            benchmark_total_pct: 基准总收益率
            benchmark_ytd_pct: 基准年化收益率
            car_pct: 超额收益率
            max_each_strategy_pct: 策略单笔交易最大收益率
            min_each_strategy_pct: 策略单笔交易最小收益率
        :return:
        """
        ap.sound(f'entry: stat_strategy')
        self.avg_stroke_pct = float(np.mean(self.l_stroke_pct))

        self.profit_num = len([i for i in self.l_stroke_pct if i > 0])
        self.profit_avg_pct = float(np.mean([i for i in self.l_stroke_pct if i > 0]))
        self.loss_num = len([i for i in self.l_stroke_pct if i <= 0])
        self.loss_avg_pct = float(np.mean([i for i in self.l_stroke_pct if i <= 0]))
        self.win_pct = self.profit_num / (self.profit_num + self.loss_num)
        self.winloss_pct = abs(sum([i for i in self.l_stroke_pct if i > 0]) / sum(
            [i for i in self.l_stroke_pct if i <= 0]))

        self.strategy_total_pct = (self.l_cum_strategy_pct[-1] - self.l_cum_strategy_pct[0]) / np.mean(
            self.l_cum_strategy_pct[0:5])
        self.strategy_ytd_pct = qp.annualized(self.strategy_total_pct, self.year_tradeday, self.kline_num)
        self.benchmark_total_pct = (self.l_close[-1] - self.l_close[0]) / np.mean(self.l_close[0:5])
        self.benchmark_ytd_pct = qp.annualized(self.benchmark_total_pct, self.year_tradeday, self.kline_num)

        self.car_pct = self.strategy_ytd_pct - self.benchmark_ytd_pct
        self.max_each_strategy_pct = max(self.l_cum_strategy_pct)
        self.min_each_strategy_pct = min(self.l_cum_strategy_pct)
        return self

    def stat_holdtime(self):
        """
        统计持仓时间相关指标:
            l_stroke_holdtime: 每一笔交易持仓时间
            avg_holdtime: 总平均持仓时间
            profit_avg_holdtime: 盈利交易平均持仓时间
            loss_avg_holdtime: 亏损交易平均持仓时间
        :return:
        """
        ap.sound(f'entry: stat_holdtime')

        self.l_stroke_holdtime = [y - x for (x, y) in self.l_holdidx]
        self.avg_holdtime = np.mean(self.l_stroke_holdtime)

        arr_stroke_pct = np.array(self.l_stroke_pct)
        arr_stroke_holdtime = np.array(self.l_stroke_holdtime)
        arr_profit = arr_stroke_holdtime[arr_stroke_pct > 0]
        arr_loss = arr_stroke_holdtime[arr_stroke_pct <= 0]
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

        mdd = qp.maxdrawdown(np.array(self.l_cum_strategy_pct))
        self.mdd_pct = mdd['ratio']
        self.mdd_range = mdd['range']

        mrg = qp.maxrevenuegrowth(np.array(self.l_cum_strategy_pct))
        self.mrg_pct = mrg['ratio']
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
        self.info_pct = qp.information_ratio(self.l_each_strategy_pct, self.l_each_benchmark_pct,
                                             self.strategy_ytd_pct, self.benchmark_ytd_pct, self.year_tradeday)
        self.benchmark_volatility = qp.volatility(self.l_each_benchmark_pct, self.year_tradeday, self.kline_num)
        self.strategy_volatility = qp.volatility(self.l_each_strategy_pct, self.year_tradeday, self.kline_num)
        self.bate = qp.bate_ratio(self.l_each_strategy_pct, self.l_each_benchmark_pct)
        self.alpha = qp.alpha_ratio(self.strategy_ytd_pct, self.benchmark_ytd_pct, self.rf, self.bate)

        return self

    def output(self):
        ap.sound(f'entry: output')
        print(f'基准总收益率: {np.round(self.benchmark_total_pct, 4)}, 策略总收益率: {np.round(self.strategy_total_pct, 4)}\n'
              f'基准年化收益率: {np.round(self.benchmark_ytd_pct, 4)}, 策略年化收益率: {np.round(self.strategy_ytd_pct, 4)}\n'
              f'年化超额收益率: {np.round(self.car_pct, 4)}, 胜率: {np.round(self.win_pct, 4)}, '
              f'盈亏比: {np.round(self.winloss_pct, 4)}\n'
              f'夏普比率: {np.round(self.sharpe_pct, 4)}, Alpha: {np.round(self.alpha, 4)}, '
              f'Bate: {np.round(self.bate, 4)}, 信息比率: {np.round(self.info_pct, 4)}\n'
              f'策略波动率: {np.round(self.strategy_volatility, 4)}, 基准波动率: {np.round(self.benchmark_volatility, 4)}\n'
              f'最高浮动收益率: {np.round(self.max_each_strategy_pct, 4)}, '
              f'最低浮动收益率: {np.round(self.min_each_strategy_pct, 4)}\n'
              f'最大回撤率: {np.round(self.mdd_pct, 4)}, 最大回撤位置: {self.mdd_range}\n'
              f'最大收益率: {np.round(self.mrg_pct, 4)}, 最大收益位置: {self.mrg_range}\n'
              f'总交易次数: {len(self.l_stroke_pct)}, 平均收益率: {np.round(self.avg_stroke_pct, 4)}, '
              f'平均持仓时间: {np.round(self.avg_holdtime, 4)}\n'
              f'盈利交易次数: {self.profit_num}, 盈利交易平均收益率: {np.round(self.profit_avg_pct, 4)}, '
              f'盈利交易平均持仓时间: {np.round(self.profit_avg_holdtime, 4)}\n'
              f'亏损交易次数: {self.loss_num}, 亏损交易平均收益率: {np.round(self.loss_avg_pct, 4)}, '
              f'亏损交易平均持仓时间: {np.round(self.loss_avg_holdtime, 4)}\n'
              f'总测试天数: {self.kline_num}, 持仓天数: {self.tradeday_num}, 持仓天数占比: {np.round(self.tradeday_pct, 2)}')

        return self

    def run(self):
        self.get_stroke_pct()
        self.stat_yield()
        self.stat_holdtime()
        self.stat_maxtrade()
        self.stat_tradeday()
        self.stat_otherindex()
        self.output()
        return self
