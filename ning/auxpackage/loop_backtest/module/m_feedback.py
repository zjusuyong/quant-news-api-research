from auxpackage.tookit import quant_package as qp
from auxpackage.tookit.analysis_package import ap
import pandas as pd
import empyrical


class FeedBack:
    def __init__(self, cls):
        self.cls = cls
        self.df = pd.DataFrame()

    def create_df(self):
        ap.sound(f'entry: create_df')

        self.df['datetime'] = self.cls.df.datetime
        self.df['eac_stgy_rt'] = self.cls.yd.eac_stgy_rt
        self.df['cum_stgy_rt'] = self.cls.yd.cum_stgy_rt
        self.df['eac_bcmk_rt'] = self.cls.yd.eac_bcmk_rt
        self.df['cum_bcmk_rt'] = self.cls.yd.cum_bcmk_rt
        self.df.set_index('datetime', inplace=True)

    def evaluation(self):
        ap.sound(f'entry: create_df')

        mdd = empyrical.max_drawdown(self.df.eac_stgy_rt)
        stgy_ret_an = empyrical.annual_return(self.df.eac_stgy_rt, annualization=self.cls.annualization)
        bcmk_ret_an = empyrical.annual_return(self.df.eac_bcmk_rt, annualization=self.cls.annualization)
        stgy_vlt_an = empyrical.annual_volatility(self.df.eac_stgy_rt, annualization=self.cls.annualization)
        bcmk_vlt_an = empyrical.annual_volatility(self.df.eac_bcmk_rt, annualization=self.cls.annualization)
        calmar = empyrical.calmar_ratio(self.df.eac_stgy_rt, annualization=self.cls.annualization)
        omega = empyrical.omega_ratio(self.df.eac_stgy_rt, risk_free=self.cls.rf, annualization=self.cls.annualization)
        sharpe = qp.sharpe_ratio(stgy_ret_an, self.df.cum_stgy_rt, self.cls.rf)
        sortino = empyrical.sortino_ratio(self.df.eac_stgy_rt, annualization=self.cls.annualization)
        dsrk = empyrical.downside_risk(self.df.eac_stgy_rt, annualization=self.cls.annualization)
        information = empyrical.information_ratio(self.df.eac_stgy_rt, factor_returns=self.df.eac_bcmk_rt)
        beta = empyrical.beta(self.df.eac_stgy_rt, factor_returns=self.df.eac_bcmk_rt, risk_free=self.cls.rf)
        tail_rt = empyrical.tail_ratio(self.df.eac_stgy_rt)
        alpha = qp.alpha_ratio(stgy_ret_an, bcmk_ret_an, self.cls.rf, beta)

        stgy_ttrt_rt = (self.cls.yd.ttas[-1] - self.cls.yd.ttas[0]) / self.cls.yd.ttas[0]
        bcmk_ttrt_rt = (self.cls.pc.close[-1] - self.cls.pc.close[0]) / self.cls.pc.close[0]
        car_rt = stgy_ttrt_rt - bcmk_ttrt_rt
        car_rt_an = stgy_ret_an - bcmk_ret_an

        self.cls.df_output = pd.DataFrame(
            {'sgty_ttrt_rt': [stgy_ttrt_rt], 'bcmk_ttrt_rt': [bcmk_ttrt_rt], 'car_rt': [car_rt],
             'stgy_ret_an': [stgy_ret_an], 'bcmk_ret_an': [bcmk_ret_an], 'car_rt_an': [car_rt_an],
             'stgy_vlt_an': [stgy_vlt_an], 'bcmk_vlt_an': [bcmk_vlt_an], 'mdd': [mdd],
             'sharpe': [sharpe], 'alpha': [alpha], 'beta': [beta], 'information': [information],
             'tail_rt': [tail_rt], 'calmar': [calmar], 'omega': [omega], 'sortino': [sortino], 'dsrk': [dsrk]})
        print(f'feedback: \n{self.cls.df_output.T}')

    def run(self):
        self.create_df()
        self.evaluation()
