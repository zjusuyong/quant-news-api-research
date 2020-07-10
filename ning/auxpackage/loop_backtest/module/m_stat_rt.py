from auxpackage.tookit.analysis_package import ap
import pandas as pd


def stgy_rt(cls):
    ap.sound(f'entry: stgy_rt')

    df = pd.DataFrame()
    df['ttas'] = cls.yd.ttas
    df['shift'] = cls.yd.ttas
    df['shift'] = df['shift'].shift(1).fillna(0)
    df['eac_stgy_rt'] = df.apply(lambda x: (x['ttas'] - x['shift']) / x['shift'] if x['shift'] != 0 else 0, axis=1)

    cls.yd.eac_stgy_rt = df.eac_stgy_rt.values
    cls.yd.cum_stgy_rt = (1 + cls.yd.eac_stgy_rt).cumprod()


def bcmk_rt(cls):
    ap.sound(f'entry: bcmk_rt')

    df = pd.DataFrame()
    df['bcmk'] = cls.df.close
    df['shift'] = cls.df.close
    df['shift'] = df['shift'].shift(1).fillna(0)
    df['eac_bcmk_rt'] = df.apply(lambda x: (x['bcmk'] - x['shift']) / x['shift'] if x['shift'] != 0 else 0, axis=1)

    cls.yd.eac_bcmk_rt = df.eac_bcmk_rt.values
    cls.yd.cum_bcmk_rt = (1 + cls.yd.eac_bcmk_rt).cumprod()
