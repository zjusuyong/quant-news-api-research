# -*- coding: UTF-8 -*-
from auxpackage.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
from auxpackage.vector_backtest.get_data import GetData
from auxpackage.vector_backtest.feedback import FeedBack
import matplotlib.pyplot as plt
import numpy as np
import talib

register_matplotlib_converters()


class HomologousStrategy:
    def __init__(self, path_r, rf=0.028, year_tradeday=250, dict_replace_columns=None):
        gd = GetData(path_r, dict_replace_columns=dict_replace_columns)
        gd.run()
        self.df = gd.df
        self.rf = rf
        self.year_tradeday = year_tradeday

        self.l_close = None
        self.l_each_close_pct = None
        self.l_signal = None
        self.l_cum_strategy_pct = None
        self.l_cum_benchmark_pct = None

    def asd_data(self):
        ap.sound(f'entry: asd_data')
        self.l_each_close_pct = self.df['close'].pct_change().tolist()
        self.l_cum_benchmark_pct = (1 + np.array(self.l_each_close_pct[1:])).cumprod()
        return self

    def idx_signal(self):
        ap.sound(f'entry: idx_signal')
        dif, dea, hist = talib.MACD(self.df['close'])
        # ema12 = talib.EMA(self.df['close'], 12)
        l_ema26 = talib.EMA(self.df['close'], 26)
        m5 = talib.SMA(self.df['close'], 5)

        self.l_signal = (hist > 0) & (dea > 0)
        return self

    def backtest(self):
        ap.sound(f'entry: backtest')
        self.l_signal = self.l_signal.shift(1).fillna(0).astype(int)
        l_signal_pct = self.l_signal * self.l_each_close_pct
        self.l_cum_strategy_pct = (1 + l_signal_pct).cumprod()
        return self

    def feedback(self):
        fb = FeedBack(self.df, self.l_each_close_pct, self.l_signal, self.l_cum_strategy_pct,
                      rf=self.rf, year_tradeday=self.year_tradeday)
        fb.run()
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
        plt.plot(self.l_cum_benchmark_pct, color='teal')
        plt.plot(self.l_cum_strategy_pct, color='grey')
        plt.legend(['benchmark', 'strategy yield curve'], loc="best")
        plt.show()
        return self

    def run(self):
        self.asd_data()
        self.idx_signal()
        self.backtest()
        self.feedback()
        self.draw_price()
        self.draw_signal()
        self.draw_back()
        ap.sound(f'finished')
        return self


if __name__ == '__main__':
    path_r_ = r'../../../data/index/hist_sz.csv'
    # path_r_ = r'../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'
    dict_replace_columns_ = None
    hm = HomologousStrategy(path_r=path_r_, dict_replace_columns=dict_replace_columns_)
    hm.run()
