# -*- coding: UTF-8 -*-
from pandas.plotting import register_matplotlib_converters
from auxpackage.vector_backtest.m1_get_data import GetData
from auxpackage.loop_backtest.role.r_yields import Yield
from auxpackage.loop_backtest.role.r_price import Price
from auxpackage.loop_backtest.role.r_account import Account
from auxpackage.loop_backtest.role.r_order import Order

register_matplotlib_converters()

path_r = r'../../../../data/index/hist_szs.csv'
year_tradeday = 250

tushare = None
dict_replace_columns = None

gd = GetData(path_r=path_r, tushare=tushare, dict_replace_columns=dict_replace_columns)
gd.run()

tcr = 0.0005
slpv = 0.01
pstp = 0.2
odv = None

df = gd.df
l_temp = df['close'].pct_change().tolist()
l_temp[0] = 0
df['cgp'] = l_temp

df = df[:20]

yd = Yield()
pc = Price()
ac = Account(10000)
od = Order()
sgn = False


def signal_longopen():
    if pc.close[-2] > pc.close[-3]:
        return True
    else:
        return False


def signal_shortopen():
    if pc.close[-2] > pc.close[-3]:
        return True
    else:
        return False


def signal_longflat():
    if pc.close[-2] > pc.close[-3]:
        return True
    else:
        return False


def signal_shortflat():
    if pc.close[-2] > pc.close[-3]:
        return True
    else:
        return False


for idx, r in df.iterrows():
    ths_yield_l = []
    ths_yield_s = []

    ths_avlb = ac.avlb[-1]
    ths_pst_l = ac.pst_l[-1]
    ths_pst_s = ac.pst_s[-1]

    """
    平仓单要点:
        1.需要判断持仓是否充足
        2.需要考虑滑点，当日收益是可执行价格-前日收盘价
        3.当日收益需要乘以负一
    """
    # 多平
    sgn_lf = signal_longflat()
    if sgn_lf:
        # 计算交易量
        if pstp:
            odv = int(ths_pst_l * pstp)
        # 判断持仓是否充足
        if ths_pst_l >= odv >= 1:
            # 计算可执行价格
            eprice = r.open - slpv
            # 计算交易额
            tsmt = odv * eprice
            # 减少多单持仓
            ths_pst_l -= odv
            # 增加可用资金
            ths_avlb += tsmt
            # 记录本次收益
            tcgp = (eprice - pc.close[-1]) / pc.close[-1]
            ths_yield_l.append(tsmt * tcgp)
            # 记录订单
            od.odl.append({'direction': 'long',
                           'operation': 'flat',
                           'vol': odv,
                           'price': eprice,
                           'transaction_amount': tsmt,
                           'trade_charge': 0})

    # 空平
    sgn_sf = signal_shortflat()
    if sgn_sf:
        # 计算交易量
        if pstp:
            odv = int(ths_pst_s * pstp)
        # 判断持仓是否充足
        if ths_pst_s >= odv >= 1:
            # 计算可执行价格
            eprice = r.open + slpv
            # 计算交易额
            tsmt = odv * eprice
            # 减少空单持仓
            ths_pst_s -= odv
            # 增加可用资金
            ths_avlb += tsmt
            # 记录本次收益
            tcgp = (eprice - pc.close[-1]) / pc.close[-1]
            ths_yield_s.append(tsmt * tcgp * -1)
            # 记录订单
            od.odl.append({'direction': 'short',
                           'operation': 'flat',
                           'vol': odv,
                           'price': eprice,
                           'transaction_amount': tsmt,
                           'trade_charge': 0})

    """
    持仓单要点:
        1.需要判断是否有持仓
        2.不需要考虑滑点和手续费
        3.收益是今日收盘价-昨日收盘价
        4.不需要调整可用资金与持仓
    """
    # 多持
    # 判断是否有持有多单
    if ths_pst_l > 0:
        # 计算交易额
        tsmt = ths_pst_l * pc.close[-1]
        # 记录本次收益
        tcgp = (r.close - pc.close[-1]) / pc.close[-1]
        ths_yield_l.append(tsmt * tcgp)

    # 空持
    # 判断是否持有空单
    if ths_pst_l > 0:
        # 计算交易额
        tsmt = ths_pst_s * pc.close[-1]
        # 记录本次收益
        tcgp = (r.close - pc.close[-1]) / pc.close[-1]
        ths_yield_s.append(tsmt * tcgp * -1)

    """
    开仓单要点:
        1.需要判断可用资金是否充足
        2.需要考虑滑点，当日收益是收盘价-可执行价格
        3.需要计算手续费
    """
    # 多开
    sgn_lo = signal_longopen()
    if sgn_lo:
        # 计算可执行价格
        eprice = r.open + slpv
        # 计算交易量
        if pstp:
            odv = int(ths_avlb * pstp / eprice)
        # 计算交易额
        tsmt = odv * eprice
        # 计算手续费
        tc = tsmt * tcr
        # 判断可用资金是否充足
        if ths_avlb >= tsmt + tc:
            # 增加多单持仓
            ths_pst_l += odv
            # 减少可用资金
            ths_avlb -= tsmt + tc
            # 记录本次收益
            tcgp = (r.close - eprice) / eprice
            ths_yield_l.append(tsmt * tcgp - tc)
            # 记录订单
            od.odl.append({'direction': 'long',
                           'operation': 'open',
                           'vol': odv,
                           'price': eprice,
                           'transaction_amount': tsmt,
                           'trade_charge': 0})

    # 空开
    sgn_so = signal_shortopen()
    if sgn_so:
        # 计算可执行价格
        eprice = r.open - slpv
        # 计算交易量
        if pstp:
            odv = int(ths_avlb * pstp / eprice)
        # 计算交易额
        tsmt = odv * eprice
        # 计算手续费
        tc = tsmt * tcr
        # 判断可用资金是否充足
        if ths_avlb >= tsmt + tc:
            # 增加空单持仓
            ths_pst_s += odv
            # 减少可用资金
            ths_avlb -= tsmt + tc
            # 记录本次收益
            tcgp = (r.close - eprice) / eprice
            ths_yield_s.append(tsmt * tcgp * -1 - tc)
            # 记录订单
            od.odl.append({'direction': 'short',
                           'operation': 'open',
                           'vol': odv,
                           'price': eprice,
                           'transaction_amount': tsmt,
                           'trade_charge': 0})

    ths_yield_l_res = sum(ths_yield_l)
    ths_yield_s_res = sum(ths_yield_s)
    ths_yield_ls_res = ths_yield_l_res + ths_yield_s_res

    ths_ttas_res = ths_avlb + (ths_pst_l + ths_pst_s) * r.close
    yd.ttas.append(ths_ttas_res)

    assert ths_ttas_res == yd.ttas[-1] + ths_yield_ls_res, \
        f'{ths_ttas_res} is not equal to {yd.ttas[-1]} + {ths_yield_ls_res}'

    pc.close.append(r.close)
    ac.avlb.append(ths_avlb)
    ac.pst_l.append(ths_pst_l)
    ac.pst_s.append(ths_pst_s)





# def flat(self, longshort, r, pstp=1, odv=None):
#     if longshort == 'long':
#         sgn = self.sg.signal_longflat()
#         ths_pst = self.ths_pst_l
#         ths_yield = self.ths_yield_l
#     else:
#         sgn = self.sg.signal_shortflat()
#         ths_pst = self.ths_pst_s
#         ths_yield = self.ths_yield_s
#
#     if sgn:
#         # 计算交易量
#         if pstp:
#             odv = int(ths_pst * pstp)
#         # 判断持仓是否充足
#         if ths_pst >= odv >= 1:
#             # 计算可执行价格
#             eprice = r.open + self.slpv
#             # 计算交易额
#             tsmt = odv * eprice
#             # 减少空单持仓
#             ths_pst -= odv
#             # 增加可用资金
#             self.ths_avlb += tsmt
#             # 记录本次收益
#             tcgp = (eprice - self.pc.close[-1]) / self.pc.close[-1]
#             ths_yield.append(tsmt * tcgp * -1)
#             # 记录订单
#             self.od.odl.append({'direction': longshort,
#                                 'operation': 'flat',
#                                 'vol': odv,
#                                 'price': eprice,
#                                 'transaction_amount': tsmt,
#                                 'trade_charge': 0})
#     if longshort == 'long':
#         self.ths_pst_l = ths_pst
#         self.ths_yield_l = ths_yield
#     else:
#         self.ths_pst_s = ths_pst
#         self.ths_yield_s = ths_yield