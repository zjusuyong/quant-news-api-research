from auxpackage.loop_backtest.role.r_signal import Signal
from auxpackage.loop_backtest.module import m_entry as et
from auxpackage.tookit import quant_package as qp
from sklearn.linear_model import LinearRegression
import talib
import numpy as np


class Strategy(Signal):

    def asd_idx(self):
        self.df['ma_13'] = talib.SMA(self.df.close, 13)
        self.df['ma_89'] = talib.SMA(self.df.close, 89)

    def signal_longopen(self, idx):
        x_train = []
        y_train = []

        df_train = self.df.close[idx - 100: idx]
        ds = qp.dataset_windows(df_train.values, window_size=50, shift=1, stride=1)
        for feature, label in ds.take(10):
            x_train.append(feature.numpy())
            y_train.append(label.numpy())

        lr = LinearRegression()
        lr.fit(x_train, y_train)
        x_test = self.df.close[idx - 100:]
        y = lr.predict(x_test.values)
        change_pct = (y - self.df.close[idx]) / self.df.close[idx]

        if change_pct > 0.05:
            self.pstp = 0.5
            return True
        elif chang_pct > 0.02:
            self.pstp = 0.2
            return True
        else:
            return False

    def signal_shortopen(self, idx):
        x_train = []
        y_train = []

        df_train = self.df.close[idx - 100: idx]
        ds = qp.dataset_windows(df_train.values, window_size=50, shift=1, stride=1)
        for feature, label in ds.take(10):
            x_train.append(feature.numpy())
            y_train.append(label.numpy())

        lr = LinearRegression()
        lr.fit(x_train, y_train)
        x_test = self.df.close[idx - 100:]
        y = lr.predict(x_test.values)
        change_pct = (y - self.df.close[idx]) / self.df.close[idx]

        if change_pct < -0.05:
            self.pstp = 0.5
            return True
        elif chang_pct < -0.02:
            self.pstp = 0.2
            return True
        else:
            return False

    def signal_longflat(self, idx):
        if not self.df.ma_13[idx] > self.df.ma_89[idx] \
                and self.df.ma_13[idx - 1] > self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_shortflat(self, idx):
        if not self.df.ma_13[idx] < self.df.ma_89[idx] \
                and self.df.ma_13[idx - 1] < self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_longstop(self, idx, trailing=False):
        pass

    def signal_shortstop(self, idx, trailing=False):
        pass


if __name__ == '__main__':
    # config
    tcr = 0.00002
    slpv = 0.01
    pstp = 1
    odv = None
    initcash = 100000
    rf = 0.04
    annualization = 252
    dict_replace_columns = {'trade_date': 'datetime'}
    tushare = {'code': '000623.SZ', 'start_datetime': '20140301', 'end_datetime': '20200101'}
    path_r = None
    num = 10

    # run
    # et.single(tcr=tcr, slpv=slpv, pstp=pstp, odv=odv, initcash=initcash, rf=rf, annualization=annualization,
    #           dict_replace_columns=dict_replace_columns, path_r=path_r, tushare=tushare)
    et.batch(tcr=tcr, slpv=slpv, pstp=pstp, odv=odv, initcash=initcash, rf=rf, annualization=annualization,
             dict_replace_columns=dict_replace_columns, path_r=path_r, tushare=tushare, num=num)
