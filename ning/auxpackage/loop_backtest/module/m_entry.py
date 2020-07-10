from auxpackage.loop_backtest.module.m_mains import Loop
from auxpackage.tookit.analysis_package import ap
import tushare as ts
import pandas as pd


def batch(tcr, slpv, pstp, odv, initcash, rf=0.04, annualization=252, dict_replace_columns=None, path_r=None,
          tushare=None, num=None):
    ap.sound(f'entry: batch')

    pro = ts.pro_api()
    df = pd.DataFrame()
    df_code = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')
    l_code = df_code['ts_code'].tolist()

    if not num:
        num = len(l_code)

    for i in range(num):
        print(f'i: {i} / {len(l_code)}')

        tushare['code'] = l_code[i]
        loops = Loop(tcr=tcr, slpv=slpv, pstp=pstp, odv=odv, initcash=initcash, rf=rf, annualization=annualization,
                     dict_replace_columns=dict_replace_columns, path_r=path_r, tushare=tushare)
        loops.run()
        loops.df_output['code'] = l_code[i]
        print(loops.df_output)

        if i == 0:
            df = loops.df_output.copy()
        else:
            df = ap.concat(df, loops.df_output)

    df.to_csv(r'../../../../../data/res.csv')


def single(tcr, slpv, pstp, odv, initcash, rf=0.04, annualization=252, dict_replace_columns=None, path_r=None,
           tushare=None):
    loops = Loop(tcr=tcr, slpv=slpv, pstp=pstp, odv=odv, initcash=initcash, rf=rf, annualization=annualization,
                 dict_replace_columns=dict_replace_columns, path_r=path_r, tushare=tushare)
    loops.run()
