# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import talib
import pandas as pd

# auth(JoinquantName, JoinquantPassword)
# l_close = get_price(
#     "000300.XSHG", start_date="2015-01-01", end_date="2018-12-31", frequency="daily", fields=['close'])['close']


path_r = r'../../../data/index/hist_sz.csv'
df = pd.read_csv(path_r, encoding='gb18030')
l_close = df[['日期', '收盘价']].set_index('日期')['收盘价']
print(f'l_close:')
print(type(l_close))
print(l_close[:3])
l_close_pct = l_close.pct_change()

plt.figure(figsize=(18, 8))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(l_close)
ax2 = plt.subplot(2, 1, 2)
ax2.plot(l_close_pct)
plt.show()

dif, dea, hist = talib.MACD(l_close)
ema12 = talib.EMA(l_close, 12)
ema26 = talib.EMA(l_close, 26)

sig1 = (hist > 0)
sig2 = (hist > 0) & (dea > 0)
sig3 = (hist > 0) & (l_close > ema26)
print(f'sig1.type: {type(sig1)}')

plt.figure(figsize=(18, 12))
ax1 = plt.subplot(4, 1, 1)
ax1.plot(l_close)
ax2 = plt.subplot(4, 1, 2)
ax2.bar(x=sig1.index, height=sig1.values)
ax3 = plt.subplot(4, 1, 3)
ax3.bar(x=sig2.index, height=sig2.values)
ax4 = plt.subplot(4, 1, 4)
ax4.bar(x=sig3.index, height=sig3.values)
plt.show()

sig2_shift = sig2.shift(1).fillna(0).astype(int)
sig2_l_close_pct = sig2_shift * l_close_pct

cum_sig2_l_close_pct = (1 + sig2_l_close_pct).cumprod()
l_close_norm = l_close / l_close[0]

plt.figure(figsize=(18, 8))
plt.plot(l_close_norm)
plt.plot(cum_sig2_l_close_pct)
plt.legend(["benchmark", "strategy cumulative l_close_pcturn"], loc="upper left")
plt.show()
