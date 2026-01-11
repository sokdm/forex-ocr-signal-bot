import numpy as np
from indicators import ema, rsi

# Fake price data (simulating EURUSD M15)
prices = np.array([
    1.1000, 1.1005, 1.1010, 1.1008, 1.1015, 1.1020,
    1.1012, 1.1018, 1.1025, 1.1020, 1.1030, 1.1035,
    1.1030, 1.1040, 1.1045, 1.1040, 1.1050, 1.1055,
    1.1050, 1.1060, 1.1065, 1.1060, 1.1070, 1.1075
])

ema50 = ema(prices, 5)     # short EMA for demo
ema200 = ema(prices, 10)   # long EMA for demo
rsi14 = rsi(prices, 5)     # short RSI for demo

print("Price  EMA50  EMA200  RSI  Signal")
print("-" * 40)

for i in range(len(prices)):
    signal = "HOLD"

    if ema50[i] > ema200[i] and rsi14[i] < 70:
        signal = "BUY"
    elif ema50[i] < ema200[i] and rsi14[i] > 30:
        signal = "SELL"

    print(f"{prices[i]:.4f} {ema50[i]:.4f} {ema200[i]:.4f} {rsi14[i]:.1f} {signal}")
