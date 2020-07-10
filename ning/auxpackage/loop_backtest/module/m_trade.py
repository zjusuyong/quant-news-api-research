def flatlong(cls, idx, r, pstp=1, odv=None):
    # 多平
    sgn_lf = cls.sg.signal_longflat(idx) | cls.sg.signal_longstop(idx)
    if sgn_lf:
        # 计算交易量
        if pstp:
            odv = int(cls.ths_pst_l * pstp)
        # 判断持仓是否充足
        if cls.ths_pst_l >= odv >= 1:
            # 计算可执行价格
            eprice = r.open - cls.slpv
            # 计算交易额
            tsmt = odv * eprice
            # 减少多单持仓
            cls.ths_pst_l -= odv
            # 增加可用资金
            cls.ths_avlb += tsmt
            # 记录本次收益
            tcgp = (eprice - cls.pc.close[-1]) / cls.pc.close[-1]
            cls.ths_yield_l.append(tsmt * tcgp)
            # 记录订单
            cls.od.odl.append({'direction': 'long',
                               'operation': 'flat',
                               'vol': odv,
                               'price': eprice,
                               'transaction_amount': tsmt,
                               'trade_charge': 0})


def flatshort(cls, idx, r, pstp=1, odv=None):
    # 空平
    sgn_sf = cls.sg.signal_shortflat(idx) & cls.sg.signal_shortstop(idx)
    if sgn_sf:
        # 计算交易量
        if pstp:
            odv = int(cls.ths_pst_s * pstp)
        # 判断持仓是否充足
        if cls.ths_pst_s >= odv >= 1:
            # 计算可执行价格
            eprice = r.open + cls.slpv
            # 计算交易额
            tsmt = odv * eprice
            # 减少空单持仓
            cls.ths_pst_s -= odv
            # 增加可用资金
            cls.ths_avlb += tsmt
            # 记录本次收益
            tcgp = (eprice - cls.pc.close[-1]) / cls.pc.close[-1]
            cls.ths_yield_s.append(tsmt * tcgp * -1)
            # 记录订单
            cls.od.odl.append({'direction': 'short',
                               'operation': 'flat',
                               'vol': odv,
                               'price': eprice,
                               'transaction_amount': tsmt,
                               'trade_charge': 0})


def holdlong(cls, r):
    # 多持
    # 判断是否有持有多单
    if cls.ths_pst_l > 0:
        # 计算交易额
        tsmt = cls.ths_pst_l * cls.pc.close[-1]
        # 记录本次收益
        tcgp = (r.close - cls.pc.close[-1]) / cls.pc.close[-1]
        cls.ths_yield_l.append(tsmt * tcgp)


def holdshort(cls, r):
    # 空持
    # 判断是否持有空单
    if cls.ths_pst_l > 0:
        # 计算交易额
        tsmt = cls.ths_pst_s * cls.pc.close[-1]
        # 记录本次收益
        tcgp = (r.close - cls.pc.close[-1]) / cls.pc.close[-1]
        cls.ths_yield_s.append(tsmt * tcgp * -1)


def openlong(cls, idx, r):
    # 多开
    sgn_lo = cls.sg.signal_longopen(idx)
    if sgn_lo:
        # 计算可执行价格
        eprice = r.open + cls.slpv
        # 计算交易量
        if cls.pstp:
            cls.odv = int(cls.ths_avlb * cls.pstp / (eprice * (cls.tcr + 1)))
            # cls.odv = int(cls.ths_avlb * cls.pstp / eprice)
        # 计算交易额
        tsmt = cls.odv * eprice
        # 计算手续费
        tcv = tsmt * cls.tcr
        # 判断可用资金是否充足
        if cls.ths_avlb >= tsmt + tcv:
            # 增加多单持仓
            cls.ths_pst_l += cls.odv
            # 减少可用资金
            cls.ths_avlb -= tsmt + tcv
            # 记录本次收益
            tcgp = (r.close - eprice) / eprice
            cls.ths_yield_l.append(tsmt * tcgp - tcv)
            # 记录订单
            cls.od.odl.append({'direction': 'long',
                               'operation': 'open',
                               'vol': cls.odv,
                               'price': eprice,
                               'transaction_amount': tsmt,
                               'trade_charge': 0})


def openshort(cls, idx, r):
    # 空开
    sgn_so = cls.sg.signal_shortopen(idx)
    if sgn_so:
        # 计算可执行价格
        eprice = r.open - cls.slpv
        # 计算交易量
        if cls.pstp:
            cls.odv = int(cls.ths_avlb * cls.pstp / (eprice * (cls.tcr + 1)))
            # cls.odv = int(cls.ths_avlb * cls.pstp / eprice)
        # 计算交易额
        tsmt = cls.odv * eprice
        # 计算手续费
        tcv = tsmt * cls.tcr
        # 判断可用资金是否充足
        if cls.ths_avlb >= tsmt + tcv:
            # 增加空单持仓
            cls.ths_pst_s += cls.odv
            # 减少可用资金
            cls.ths_avlb -= tsmt + tcv
            # 记录本次收益
            tcgp = (r.close - eprice) / eprice
            cls.ths_yield_s.append(tsmt * tcgp * -1 - tcv)
            # 记录订单
            cls.od.odl.append({'direction': 'short',
                               'operation': 'open',
                               'vol': cls.odv,
                               'price': eprice,
                               'transaction_amount': tsmt,
                               'trade_charge': 0})
