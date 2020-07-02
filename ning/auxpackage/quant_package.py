import numpy as np
import math


def maxdrawdown(arr):
    """
    计算最大回撤值
    :param arr: 收益率np数组
    :return: dict: {'ratio': 最大回撤比率, 'range': [开始位置, 结束位置]}
    """
    i = np.argmax((np.maximum.accumulate(arr) - arr) / np.maximum.accumulate(arr))
    j = np.argmax(arr[:i])
    return {'ratio': (1 - arr[i] / arr[j]), 'range': [j, i]}


def maxrevenuegrowth(arr):
    """
    计算最大收益
    :param arr: 收益率np数组
    :return: dict: {'ratio': 最大收益比率, 'range': [开始位置, 结束位置]}
    """
    i = np.argmax((arr - np.minimum.accumulate(arr)) / np.minimum.accumulate(arr))
    j = np.argmin(arr[:i])
    return {'ratio': (arr[i] / arr[j] - 1), 'range': [j, i]}


def volatility(l_each_pct, year_tradeday, kline_num):
    """
    计算波动率
    :param l_each_pct: list, 每一Kline的pct_change
    :param year_tradeday: 每年交易天数
    :param kline_num: 测试数据总Kline数量
    :return:
    """
    series_diff = l_each_pct - np.mean(l_each_pct)
    # temp = series_diff.map(lambda x: math.pow(x, 2)).sum()
    temp = np.sum(series_diff**2)
    return np.sqrt(temp * year_tradeday / (kline_num - 1))


def information_ratio(l_each_strategy_pct, l_each_benchmark_pct, strategy_ytd_pct, benchmark_ytd_pct, year_tradeday):
    """
    计算信息比率
    :param l_each_strategy_pct: list, 策略每一Kline的pcg_change
    :param l_each_benchmark_pct: list, 基准每一Kline的pcg_change
    :param strategy_ytd_pct: 策略年华收益率
    :param benchmark_ytd_pct: 基准年华收益率
    :param year_tradeday: 每年交易天数
    :return:
    """
    year_proyield_std = np.sqrt(year_tradeday) * np.std(np.array(l_each_strategy_pct) - np.array(l_each_benchmark_pct))
    return (strategy_ytd_pct - benchmark_ytd_pct) / year_proyield_std


def sharpe_ratio(strategy_ytd_pct, l_cum_strategy_pct, rf):
    """
    计算夏普比率
    :param strategy_ytd_pct: 策略年化收益率
    :param l_cum_strategy_pct: series, 策略累计收益率
    :param rf: 无风险利率
    :return:
    """
    return (strategy_ytd_pct - rf) / np.std(l_cum_strategy_pct.values, ddof=1)

# todo: 这里的l_each_strategy_pct应该吧没有的地方填上0，补成和l_each_benchmark_pct同等长度
def bate(l_each_strategy_pct, l_each_benchmark_pct):
    """
    计算贝塔值
    :param l_each_strategy_pct: list, 策略每一Kline的pcg_change
    :param l_each_benchmark_pct: list, 基准每一Kline的pcg_change
    :return:
    """
    return np.cov(l_each_strategy_pct, l_each_benchmark_pct) / np.var(l_each_benchmark_pct)


def alpha(strategy_ytd_pct, benchmark_ytd_pct, rf, bate):
    """
    计算alpha
    :param strategy_ytd_pct: 策略年化收益率
    :param benchmark_ytd_pct: 基准年华收益率
    :param rf: 无风险利率
    :param bate: beta值
    :return:
    """
    return strategy_ytd_pct - rf - bate * (benchmark_ytd_pct - rf)


def total_annualized_returns(total_returns, year_tradeday, kline_num):
    """
    计算年华收益率
    :param total_returns: 总收益
    :param year_tradeday: 每年交易天数
    :param kline_num: 测试数据总Kline数量
    :return:
    """
    return math.pow(1 + total_returns, year_tradeday / kline_num) - 1
