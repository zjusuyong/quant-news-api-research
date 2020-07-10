from auxpackage.vector_backtest.m0_homologous_strategy import HomologousStrategy
from auxpackage.tookit.analysis_package import ap
import pandas as pd
import tushare as ts
import talib


class HSStrategy(HomologousStrategy):
    def idx_signal(self):
        l_sma13 = talib.SMA(self.l_close, 13)
        l_sma89 = talib.SMA(self.l_close, 89)
        self.l_signal = (self.l_close > l_sma13) & (l_sma13 > l_sma89)


def process(tushare, dict_replace_columns, year_tradeday=25, path_r=None):
    ap.sound(f'entry: process')

    pro = ts.pro_api()
    df = pd.DataFrame()

    df_code = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')
    l_code = df_code['ts_code'].tolist()

    # for i in range(len(l_code)):
    for i in range(200):
        print(f'i: {i} / {len(l_code)}')

        tushare['code'] = l_code[i]
        hss = HSStrategy(year_tradeday=year_tradeday, path_r=path_r,
                         tushare=tushare, dict_replace_columns=dict_replace_columns)
        hss.run()
        hss.df_output['code'] = l_code[i]
        print(hss.df_output)
        if i == 0:
            df = hss.df_output.copy()
        else:
            df = ap.concat(df, hss.df_output)

    df.to_csv(r'../../../../data/res.csv')


if __name__ == '__main__':
    tushare_ = {'code': '', 'start_datetime': '20010101', 'end_datetime': '20200601'}
    dict_replace_columns_ = {'trade_date': 'datetime'}
    year_tradeday_ = 250

    process(tushare=tushare_, dict_replace_columns=dict_replace_columns_, year_tradeday=year_tradeday_)
