from auxpackage.vector_backtest.m0_homologous_strategy import HomologousStrategy
import talib


class HSStrategy(HomologousStrategy):
    def idx_signal(self):
        dif, dea, hist = talib.MACD(self.l_close)
        l_ema26 = talib.EMA(self.l_close, 26)
        self.l_signal = (hist > 0) & (self.l_close > l_ema26)


if __name__ == '__main__':
    path_r_ = r'../../../data/index/hist_szs.csv'
    tushare_ = None
    dict_replace_columns_ = None
    year_tradeday_ = 252

    hss = HSStrategy(year_tradeday=year_tradeday_, path_r=path_r_,
                     tushare=tushare_, dict_replace_columns=dict_replace_columns_)
    hss.run()
