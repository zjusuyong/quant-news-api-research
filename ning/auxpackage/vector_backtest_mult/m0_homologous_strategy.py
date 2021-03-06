# -*- coding: UTF-8 -*-
from auxpackage.tookit.analysis_package import ap
from auxpackage.tookit import quant_package as qp
from pandas.plotting import register_matplotlib_converters
from auxpackage.vector_backtest.m1_get_data import GetData
from auxpackage.vector_backtest.m2_feedback import FeedBack
from auxpackage.vector_backtest import m3_draw as dr
import numpy as np

register_matplotlib_converters()


class HomologousStrategy:
    def __init__(self, rf=0.04, year_tradeday=250, path_r=None, tushare=None, dict_replace_columns=None):
        gd = GetData(path_r=path_r, tushare=tushare, dict_replace_columns=dict_replace_columns)
        gd.run()
        self.df = gd.df
        self.rf = rf
        self.year_tradeday = year_tradeday

        self.fb = None
        self.l_close = None
        self.l_each_close_pct = None
        self.l_each_benchmark_pct = None
        self.l_each_strategy_pct = None

        self.l_signal_longopen = None
        self.l_signal_longflat = None
        self.l_signal_shortopen = None
        self.l_signal_shortflat = None
        self.l_signal_long = None
        self.l_signal_short = None
        self.l_signal = None

        self.l_each_strategy_long_pct = None
        self.l_each_strategy_short_pct = None

        self.l_cum_strategy_pct = None
        self.l_cum_benchmark_pct = None

    def asd_benchmark(self):
        ap.sound(f'entry: asd_data')
        self.l_close = self.df['close'].copy()
        self.l_each_close_pct = self.l_close.pct_change().tolist()
        self.l_each_benchmark_pct = self.l_each_close_pct
        self.l_each_benchmark_pct[0] = 0
        self.l_cum_benchmark_pct = (1 + np.array(self.l_each_benchmark_pct)).cumprod()
        return self

    def idx_signal(self):
        ap.sound(f'entry: idx_signal')
        # l_sma13 = talib.SMA(self.l_close, 13)
        # l_sma89 = talib.SMA(self.l_close, 89)
        # self.l_signal_longopen = (self.l_close > l_sma13) & (l_sma13 > l_sma89)
        # self.l_signal_longflat = (self.l_close < l_sma13)
        return self

    def backtest(self):
        ap.sound(f'entry: backtest')
        if not self.l_signal_long:
            self.l_signal_long = np.zeros(len(self.l_close))
        if not self.l_signal_short:
            self.l_signal_short = np.zeros(len(self.l_close))

        self.l_signal_long = qp.get_signal(self.l_signal_longopen, self.l_signal_longflat)
        self.l_signal_long = self.l_signal_long.shift(1).fillna(0).astype(int)

        self.l_signal_short = qp.get_signal(self.l_signal_shortopen, self.l_signal_shortflat)
        self.l_signal_short = self.l_signal_short.shift(1).fillna(0).astype(int)

        self.l_signal = np.array(self.l_signal_long) + np.array(self.l_signal_short)
        self.l_signal[self.l_signal == 2] = 1

        self.l_each_strategy_long_pct = self.l_signal_long * self.l_each_benchmark_pct
        self.l_each_strategy_short_pct = self.l_signal_short * self.l_each_benchmark_pct * -1

        self.l_each_strategy_pct = self.l_each_strategy_long_pct + self.l_each_strategy_short_pct
        self.l_cum_strategy_pct = (1 + np.array(self.l_each_strategy_pct)).cumprod()
        return self

    def feedback(self):
        self.fb = FeedBack(self.df, self.l_signal, self.l_each_benchmark_pct, self.l_each_strategy_pct,
                           self.l_cum_strategy_pct, rf=self.rf, year_tradeday=self.year_tradeday)
        self.fb.run()
        return self

    def run(self):
        self.asd_benchmark()
        self.idx_signal()
        self.backtest()
        self.feedback()
        # dr.draw_price(self.l_close, self.l_each_benchmark_pct)
        # dr.draw_signal(self.l_close, self.l_signal)
        # dr.draw_srtoke_distribution(self.fb.l_stroke_holdtime, self.fb.l_stroke_pct)
        # dr.draw_back(np.array(self.l_close), self.l_cum_strategy_pct)
        ap.sound(f'finished')
        return self


if __name__ == '__main__':
    path_r_ = r'../../../../data/index/hist_szs.csv'
    # path_r_ = r'../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'
    # tushare_ = {'code': '000001.SZ', 'start_datetime': '20190101', 'end_datetime': '20190630'}
    tushare_ = None
    dict_replace_columns_ = None

    hs = HomologousStrategy(path_r=path_r_, tushare=tushare_, dict_replace_columns=dict_replace_columns_)
    hs.run()
