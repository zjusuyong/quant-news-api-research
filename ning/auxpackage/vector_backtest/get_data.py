# -*- coding: UTF-8 -*-
from auxpackage.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
import pandas as pd
import tushare as ts

register_matplotlib_converters()


class GetData:
    def __init__(self, path_r, dict_replace_columns=None):
        self.path_r = path_r
        self.dict_replace_columns = dict_replace_columns
        self.df = None


    def get_data(self):
        ap.sound(f'entry: get_data')
        df = pd.read_csv(self.path_r, encoding='gb18030')
        # self.df = self.df.set_index('datetime')
        # print(f'df: \n{self.df.head()}')

        # token = '31e528be4a85855ac2408fb477b2e9bd0f083e53461f1119d6e9619f'
        # pro = ts.pro_api(token)

        # df = pro.daily(ts_code='000001.SZ', start_date='20190101', end_date='20190630')
        if self.dict_replace_columns:
            df.rename(columns=self.dict_replace_columns, inplace=True)
        self.df = df[['datetime', 'close']].copy()
        self.df.sort_values(by='datetime', inplace=True)
        self.df = self.df.set_index('datetime')
        return self

    def run(self):
        self.get_data()
        return self
