from auxpackage.vector_backtest.m0_homologous_strategy import HomologousStrategy
import talib


class HSStrategy(HomologousStrategy):
    def idx_signal(self):
        dif, dea, hist = talib.MACD(self.l_close)
        ema12 = talib.EMA(self.df['close'], 12)
        l_ema26 = talib.EMA(self.l_close, 26)
        m5 = talib.SMA(self.l_close, 5)
        self.l_signal = (dea < 0)
        return self

if __name__ == '__main__':
    path_r_ = r'../../../../data/index/hist_szs.csv'
    # path_r_ = r'../../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'
    # tushare_ = {'code': '000001.SZ', 'start_datetime': '20190101', 'end_datetime': '20190630'}
    tushare_ = None
    dict_replace_columns_ = None
    year_tradeday_ = 360000

    hss = HSStrategy(year_tradeday=year_tradeday_, path_r=path_r_,
                     tushare=tushare_, dict_replace_columns=dict_replace_columns_)
    hss.run()