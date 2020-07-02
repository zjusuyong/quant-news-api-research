# -*- coding: UTF-8 -*-
from auxpackage.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
from auxpackage import quant_package as qp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import talib
import tushare as ts

register_matplotlib_converters()


class MACD:
    def __init__(self, path_r):
        self.path_r = path_r
        self.df = None
        self.l_close = None
        self.l_each_close_pct = None
        self.l_signal = None
        self.l_yield = None
        self.l_close_norm = None

    def get_data(self):
        ap.sound(f'entry: get_data')
        self.df = pd.read_excel(self.path_r, encoding='gb18030')
        self.df = self.df.set_index('datetime')
        print(f'df: \n{self.df.head()}')

        token = '31e528be4a85855ac2408fb477b2e9bd0f083e53461f1119d6e9619f'
        pro = ts.pro_api(token)

        # df = pro.daily(ts_code='000001.SZ', start_date='20190101', end_date='20190630')
        # print(df.head())
        # self.df = df[['trade_date', 'pre_close']].copy()
        # self.df.rename(columns={'trade_date': 'datetime', 'pre_close': 'close'}, inplace=True)
        # self.df.sort_values(by='datetime', inplace=True)
        # self.df = self.df.set_index('datetime')
        return self

    def asd_data(self):
        ap.sound(f'entry: asd_data')
        self.l_each_close_pct = self.df['close'].pct_change().tolist()
        return self

    def idx_signal(self):
        ap.sound(f'entry: idx_signal')
        dif, dea, hist = talib.MACD(self.df['close'])
        # ema12 = talib.EMA(self.df['close'], 12)
        l_ema26 = talib.EMA(self.df['close'], 26)
        m5 = talib.SMA(self.df['close'], 5)
        self.l_signal = (hist < 0) & (dea < 0)
        return self

    def backtest(self):
        ap.sound(f'entry: backtest')
        self.l_signal = self.l_signal.shift(1).fillna(0).astype(int)
        l_signal_pct = self.l_signal * self.l_each_close_pct
        self.l_yield = (1 + l_signal_pct).cumprod()
        self.l_close_norm = (1 + np.array(self.l_each_close_pct[1:])).cumprod()
        return self

    def feedback(self):
        ap.sound(f'entry: feedback')

        df_feedback = pd.DataFrame()
        df_feedback['arr'] = self.l_signal
        df_feedback['arr_shift'] = self.l_signal
        df_feedback['arr_shift'] = df_feedback['arr_shift'].shift(1).fillna(0).astype(int)
        df_feedback['aux'] = df_feedback['arr'] - df_feedback['arr_shift']
        df_feedback = df_feedback.reset_index()
        df_target = df_feedback[['aux']][df_feedback['aux'] != 0].reset_index().copy()

        print(f'df_target: {df_target.head()}')
        if df_target.loc[len(df_target) - 1, 'aux'] == 1:
            df_target = ap.concat(df_target,
                                  pd.DataFrame({'index': [df_target['index'].tolist()[-1] + 1], 'aux': [-1]}))
        l_aux = df_target['index'].tolist()

        step = 2
        l_holdidx = [l_aux[i:i + step] for i in range(0, len(l_aux), step)]

        l_each_yield = [sum(self.l_each_close_pct[x:y]) for (x, y) in l_holdidx]
        avg_yield = float(np.mean(l_each_yield))

        profit_num = len([i for i in l_each_yield if i > 0])
        profit_avg_ratio = float(np.mean([i for i in l_each_yield if i > 0]))
        loss_num = len([i for i in l_each_yield if i < 0])
        loss_avg_ratio = float(np.mean([i for i in l_each_yield if i < 0]))

        l_each_holdtime = [y - x for (x, y) in l_holdidx]
        avg_holdtime = np.mean(l_each_holdtime)

        arr_each_yield = np.array(l_each_yield)
        arr_each_holdtime = np.array(l_each_holdtime)
        arr_profit = arr_each_holdtime[arr_each_yield > 0]
        arr_loss = arr_each_holdtime[arr_each_yield < 0]
        profit_avg_holdtime = np.mean(arr_profit)
        loss_avg_holdtime = np.mean(arr_loss)

        mdd = qp.maxdrawdown(np.array(self.l_yield[1:]))
        mdd_ratio = mdd['ratio'] * 100
        mdd_range = mdd['range']

        mrg = qp.maxrevenuegrowth(np.array(self.l_yield[1:]))
        mrg_ratio = mrg['ratio'] * 100
        mrg_range = mrg['range']

        yields = (self.l_yield[-1] - 1) * 100
        benchmark = (self.df['close'][-1] - self.df['close'][0]) / self.df['close'][0] * 100
        max_yield = max(self.l_yield[1:]) * 100
        min_yield = min(self.l_yield[1:]) * 100

        # todo: 改成 （年化收益率 - 利率） / 标准差
        sharpe_ratio = yields / 100 / np.std(self.l_yield, ddof=1)

        tradeday_num = len([i for i in self.l_signal if i == 1])
        tradeday_ratio = tradeday_num / len(self.l_signal) * 100

        print(f'基准收益率: {round(benchmark, 2)}%, 策略收益率: {round(yields, 2)}%, 夏普比率: {sharpe_ratio}\n'
              f'最高浮动收益率: {round(max_yield, 2)}%, 最低浮动收益率: {round(min_yield, 2)}%\n'
              f'最大回撤率: {round(mdd_ratio, 2)}%, 最大回撤位置: {mdd_range}\n'
              f'最大收益率: {round(mrg_ratio, 2)}%, 最大收益位置: {mrg_range}\n'
              f'总交易次数: {len(l_each_yield)}, 平均收益率: {round(avg_yield, 5)}%, 平均持仓时间: {avg_holdtime}\n'
              f'盈利交易次数: {profit_num}, 盈利交易平均收益率: {round(profit_avg_ratio, 5)}%, 盈利交易平均持仓时间: {profit_avg_holdtime}\n'
              f'亏损交易次数: {loss_num}, 亏损交易平均收益率: {round(loss_avg_ratio, 5)}%, 亏损交易平均持仓时间: {loss_avg_holdtime}\n'
              f'总测试天数: {len(self.l_signal)}, 持仓天数: {tradeday_num}, 持仓天数占比: {round(tradeday_ratio, 2)}%')

        dfs = pd.DataFrame()
        dfs['holdtime'] = l_each_holdtime
        dfs['yield'] = l_each_yield
        with sns.axes_style("dark"):
            # sns.jointplot('holdtime', 'yield', data=dfs,
            #               kind='reg', color='grey', space=0, ratio=6,
            #               marginal_kws={'bins': 20}, scatter={'s': 3})
            sns.jointplot('holdtime', 'yield', data=dfs,
                          kind='kde', color='grey', space=0, ratio=6)
        plt.show()
        return self

    def draw_price(self):
        ap.sound(f'entry: draw_price')
        plt.figure(figsize=(18, 8))
        ax_close = plt.subplot(2, 1, 1)
        ax_close.plot(self.df['close'], color='teal')
        ax_pct = plt.subplot(2, 1, 2)
        ax_pct.plot(self.l_each_close_pct, color='grey')
        plt.show()
        return self

    def draw_signal(self):
        ap.sound(f'entry: draw_signal')
        plt.figure(figsize=(18, 12))
        ax_close = plt.subplot(2, 1, 1)
        ax_close.plot(self.df['close'], color='teal')
        ax_signal = plt.subplot(2, 1, 2)
        ax_signal.bar(x=self.l_signal.index, height=self.l_signal.values, color='grey')
        plt.show()
        return self

    def draw_back(self):
        ap.sound(f'entry: draw_back')
        plt.figure(figsize=(18, 8))
        plt.plot(self.l_close_norm, color='teal')
        plt.plot(self.l_yield, color='grey')
        plt.legend(['benchmark', 'strategy yield curve'], loc="best")
        plt.show()
        return self

    def run(self):
        self.get_data()
        self.asd_data()
        self.idx_signal()
        self.backtest()
        self.feedback()
        # self.draw_price()
        # self.draw_signal()
        self.draw_back()
        ap.sound(f'finished')
        return self


if __name__ == '__main__':
    # path_r_ = r'../../../data/index/hist_sz.csv'
    path_r_ = r'../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'

    m = MACD(path_r=path_r_)
    m.run()
