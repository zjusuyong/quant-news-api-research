from auxpackage.vector_backtest.m0_homologous_strategy import HomologousStrategy
import numpy as np
import talib


class HSStrategy(HomologousStrategy):
    def idx_signal(self):
        h_line, m_line, l_line = talib.BBANDS(self.l_close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        dis = h_line - l_line
        self.l_signal = (self.l_close > m_line) & (dis < np.mean(dis))
        return self


if __name__ == '__main__':
    path_r_ = r'../../../data/index/hist_szs.csv'
    # path_r_ = r'../../../../data/aud&nzd/HISTDATA_COM_XLSX_AUDNZD_M12019/AUDNZD_M1_2019.xlsx'
    # tushare_ = {'code': '000001.SZ', 'start_datetime': '20190101', 'end_datetime': '20190630'}
    tushare_ = None
    dict_replace_columns_ = None
    year_tradeday_ = 250

    hss = HSStrategy(year_tradeday=year_tradeday_, path_r=path_r_,
                     tushare=tushare_, dict_replace_columns=dict_replace_columns_)
    hss.run()
