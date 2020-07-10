from auxpackage.loop_backtest.role.r_price import Price
import talib


class Signal:
    def __init__(self, df):
        self.df = df
        self.pc = Price()
        self.odv = None
        self.pstp = None

    def asd_idx(self):
        self.df['ma_13'] = talib.SMA(self.df.close, 13)
        self.df['ma_89'] = talib.SMA(self.df.close, 89)

    def signal_longopen(self, idx, flatprice=None):
        if self.df.close[idx] < flatprice:
            return True
        elif self.df.ma_13[idx] > self.df.ma_89[idx] \
                and not self.df.ma_13[idx - 1] > self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_shortopen(self, idx, flatprice=None):
        if self.df.close[idx] > flatprice:
            return True
        elif self.df.close[idx] < self.df.ma_13[idx] < self.df.ma_89[idx] \
                and not self.df.close[idx - 1] < self.df.ma_13[idx - 1] < self.df.ma_89[idx - 1]:
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
        if not self.df.close[idx] < self.df.ma_13[idx] < self.df.ma_89[idx] \
                and self.df.close[idx - 1] < self.df.ma_13[idx - 1] < self.df.ma_89[idx - 1]:
            return True
        else:
            return False

    def signal_longstop(self, idx, trailing=False):
        pass

    def signal_shortstop(self, idx, trailing=False):
        pass
