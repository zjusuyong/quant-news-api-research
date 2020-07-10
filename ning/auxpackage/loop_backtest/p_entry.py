from auxpackage.loop_backtest.module.m_mains import Loop

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

loops = Loop(tcr=tcr, slpv=slpv, pstp=pstp, odv=odv, initcash=initcash, rf=rf, annualization=annualization,
      dict_replace_columns=dict_replace_columns, path_r=path_r, tushare=tushare)
loops.run()
