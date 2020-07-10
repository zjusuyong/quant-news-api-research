# -*- coding: UTF-8 -*-
from auxpackage.tookit.analysis_package import ap
from auxpackage.loop_backtest.role.r_yields import Yield
from auxpackage.loop_backtest.role.r_price import Price
from auxpackage.loop_backtest.role.r_account import Account
from auxpackage.loop_backtest.role.r_order import Order
from auxpackage.loop_backtest.role.r_signal import Signal
from auxpackage.loop_backtest.module.m_feedback import FeedBack
from auxpackage.loop_backtest.module.m_data import GetData
from auxpackage.loop_backtest.module import m_trade as td
from auxpackage.loop_backtest.module import m_stat_rt as sr


class Loop:
    def __init__(self, tcr, slpv, pstp, odv, initcash, rf=0.04, annualization=252,
                 dict_replace_columns=None, path_r=None, tushare=None):

        self.tcr = tcr
        self.slpv = slpv
        self.pstp = pstp
        self.odv = odv
        self.rf = rf
        self.annualization = annualization

        gd = GetData(path_r=path_r, tushare=tushare, dict_replace_columns=dict_replace_columns)
        gd.run()
        self.df = self.sg.df

        self.sg = Signal(gd.df)
        self.ac = Account(initcash)
        self.yd = Yield()
        self.pc = Price()
        self.od = Order()

        self.sg.asd_idx()
        self.df_output = None
        self.ths_avlb = None
        self.ths_pst_l = None
        self.ths_pst_s = None
        self.ths_yield_l = None
        self.ths_yield_s = None

    def ondata(self):
        ap.sound(f'entry: ondata')

        for idx, r in self.df.iterrows():
            if idx % 500 == 0:
                print(f'{idx} / {len(self.df)}')
            idx -= 1

            self.ths_yield_l = [0]
            self.ths_yield_s = [0]

            self.ths_avlb = self.ac.avlb[-1]
            self.ths_pst_l = self.ac.pst_l[-1]
            self.ths_pst_s = self.ac.pst_s[-1]

            if idx > 0:
                td.flatlong(self, idx, r)
                td.flatshort(self, idx, r)
                td.holdlong(self, r)
                td.holdshort(self, r)
                td.openlong(self, idx, r)
                td.openshort(self, idx, r)

            ths_yield_ls_res = sum(self.ths_yield_l) + sum(self.ths_yield_s)
            ths_ttas_res = self.ths_avlb + (self.ths_pst_l + self.ths_pst_s) * r.close

            self.pc.close.append(r.close)
            self.yd.ttas.append(ths_ttas_res)
            self.yd.eac_ls_pf.append(ths_yield_ls_res)
            self.yd.eac_l_pf.append(sum(self.ths_yield_l))
            self.yd.eac_s_pf.append(sum(self.ths_yield_s))
            self.ac.avlb.append(self.ths_avlb)
            self.ac.pst_l.append(self.ths_pst_l)
            self.ac.pst_s.append(self.ths_pst_s)

    def stat_rt(self):
        ap.sound(f'entry: stat_rt')
        sr.stgy_rt(self)
        sr.bcmk_rt(self)

    def feedback(self):
        ap.sound(f'entry: feedback')
        fb = FeedBack(self)
        fb.run()

    def draw(self):
        # dr.draw_price(self.l_close, self.l_each_benchmark_pct)
        # dr.draw_signal(self.l_close, self.l_signal)
        # dr.draw_srtoke_distribution(self.fb.l_stroke_holdtime, self.fb.l_stroke_pct)
        # dr.draw_back(self.yd.cum_bcmk_rt, self.yd.cum_stgy_rt)
        pass

    def run(self):
        self.ondata()
        self.stat_rt()
        self.feedback()
        self.draw()
        ap.sound(f'finished')

# todo: 所有平仓单分别压入盈亏列表，统计胜率等指标
