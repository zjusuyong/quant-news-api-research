from auxpackage.vector_backtest.m0_homologous_strategy import HomologousStrategy
import talib


class HSStrategy(HomologousStrategy):
    def idx_signal(self):
        l_sma13 = talib.SMA(self.l_close, 13)
        l_sma89 = talib.SMA(self.l_close, 89)
        self.l_signal = (self.l_close > l_sma13) & (l_sma13 > l_sma89)

        # todo: 下边是给mult用的
        # l_sma13 = talib.SMA(self.l_close, 13)
        # l_sma89 = talib.SMA(self.l_close, 89)
        # self.l_signal_longopen = (self.l_close > l_sma13) & (l_sma13 > l_sma89)
        # self.l_signal_longflat = (self.l_close < l_sma13)
        #
        # self.l_signal_shortopen = (self.l_close > l_sma13) & (l_sma13 > l_sma89)
        # self.l_signal_shortflat = (self.l_close < l_sma13)
        return self


if __name__ == '__main__':
    # path_r_ = r'../../../data/index/hist_szs.csv'
    # path_r_ = r'../../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'
    path_r_ = None

    tushare_ = {'code': '000623.SZ', 'start_datetime': '20050105', 'end_datetime': '20200601'}
    # tushare_ = None

    dict_replace_columns_ = {'trade_date': 'datetime'}
    # dict_replace_columns_ = None
    year_tradeday_ = 250

    hss = HSStrategy(year_tradeday=year_tradeday_, path_r=path_r_,
                     tushare=tushare_, dict_replace_columns=dict_replace_columns_)
    hss.run()
