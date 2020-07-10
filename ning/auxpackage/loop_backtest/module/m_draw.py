# -*- coding: UTF-8 -*-
from auxpackage.tookit.analysis_package import ap
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

register_matplotlib_converters()


def draw_price(l_close, l_each_benchmark_pct):
    """
    画出基准曲线图
    :param l_close: DataFrame.Series, 收盘价列表
    :param l_each_benchmark_pct: list, 基准每个Kline的change_pct
    :return:
    """
    ap.sound(f'entry: draw_price')
    plt.figure(figsize=(18, 8))
    ax_close = plt.subplot(2, 1, 1)
    ax_close.plot(l_close, color='teal')
    ax_pct = plt.subplot(2, 1, 2)
    ax_pct.plot(l_each_benchmark_pct, color='grey')
    plt.show()


def draw_signal(l_close, l_signal):
    """
    画出基准价格和信号
    :param l_close: DataFrame.Series, 收盘价列表
    :param l_signal: DataFrame.Series, 信号列表
    :return:
    """
    ap.sound(f'entry: draw_signal')
    plt.figure(figsize=(18, 8))
    ax_close = plt.subplot(2, 1, 1)
    ax_close.plot(l_close, color='teal')
    ax_signal = plt.subplot(2, 1, 2)
    ax_signal.bar(x=l_signal.index, height=l_signal.values, color='grey')
    plt.show()


def draw_back(l_cum_benchmark_pct, l_cum_strategy_pct):
    """
    画出策略收益曲线和基准收益曲线
    :param l_cum_benchmark_pct: array, 累计基准收益率
    :param l_cum_strategy_pct: array, 累计策略收益率
    :return:
    """
    ap.sound(f'entry: draw_back')
    plt.figure(figsize=(18, 8))
    plt.plot(l_cum_benchmark_pct, color='teal')
    plt.plot(l_cum_strategy_pct, color='grey')
    plt.legend(['benchmark', 'strategy yield curve'], loc="best")
    plt.show()


def draw_srtoke_distribution(l_stroke_holdtime, l_stroke_pct):
    """
    画出每一笔交易的收益和持仓时间分布图
    :param l_stroke_holdtime: array, 每笔交易的持有时间列表
    :param l_stroke_pct: array, 每笔交易的收益
    :return:
    """
    ap.sound(f'entry: draw_srtoke_distribution')
    df = pd.DataFrame()
    df['holdtime'] = l_stroke_holdtime
    df['strategy'] = l_stroke_pct
    with sns.axes_style("dark"):
        sns.jointplot('holdtime', 'strategy', data=df,
                      kind='kde', color='grey', space=0, pct=6)
    plt.show()
