# -*- coding: UTF-8 -*-
from auxpackage.tookit.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
from configure.config import *
import pandas as pd
import tushare as ts

register_matplotlib_converters()


class GetData:
    def __init__(self, path_r=None, tushare=None, dict_replace_columns=None):
        """
        读取数据
        :param path_r: 读取csv路径
        :param tushare: dict, eg: {'code': '000001.SZ', 'start_datetime': '20190101', 'end_datetime': '20190630'}
        :param dict_replace_columns: dict, eg: {'trade_date': 'datetime', 'pre_close': 'close'}
        """
        self.path_r = path_r
        self.tushare = tushare
        self.dict_replace_columns = dict_replace_columns
        self.df = None

    def get_data(self):
        ap.sound(f'entry: get_data')
        if self.path_r:
            self.df = pd.read_csv(self.path_r, encoding='gb18030')
        elif self.tushare:
            ts.pro_api(TushareToken)
            self.df = ts.pro_bar(ts_code=self.tushare['code'],
                                 start_date=self.tushare['start_datetime'],
                                 end_date=self.tushare['end_datetime'],
                                 adj='qfq', asset='E', freq='D')
        else:
            print(f'ERROR: Input read path is empty')
        print(f'columns_name: {self.df.columns.tolist()}')
        return self

    def data_process(self):
        ap.sound(f'entry: get_data')

        if self.dict_replace_columns:
            self.df.rename(columns=self.dict_replace_columns, inplace=True)

        self.df = self.df[['datetime', 'open', 'high', 'low', 'close']].copy()
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df.sort_values(by='datetime', inplace=True)
        # self.df = self.df.set_index('datetime')
        # self.df.to_csv(r'../../../../data/20200708.csv')
        print(f'df: \n{self.df.head()}')
        return self

    def run(self):
        self.get_data()
        self.data_process()
        return self
