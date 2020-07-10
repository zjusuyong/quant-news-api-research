from auxpackage.loop_backtest.role.r_signal import Signal
from auxpackage.loop_backtest.module import m_entry as et
import talib


class Strategy(Signal):

    def asd_idx(self):
        self.df['ma_13'] = talib.SMA(self.df.close, 13)
        self.df['ma_89'] = talib.SMA(self.df.close, 89)
        self.df = self.df.reset_index(drop=True)

    def signal_longopen(self, idx):
        if self.df.ma_13[idx] > self.df.ma_89[idx] \
                and not self.df.ma_13[idx - 1] > self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_shortopen(self, idx):
        if self.df.close[idx] < self.df.ma_13[idx] < self.df.ma_89[idx] \
                and not self.df.close[idx - 1] < self.df.ma_13[idx - 1] < self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_longflat(self, idx):
        if not self.df.ma_13[idx] >= self.df.ma_89[idx] \
                and self.df.ma_13[idx - 1] > self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_shortflat(self, idx):
        if not self.df.close[idx] < self.df.ma_13[idx] < self.df.ma_89[idx] \
                and self.df.close[idx - 1] < self.df.ma_13[idx - 1] < self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_longtrailingstop(self, idx, trailing=False):
        pass

    def signal_shorttrailingstop(self, idx, trailing=False):
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
