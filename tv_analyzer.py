import numpy as np
from indicators import ema, rsi

# Example TradingView alert input (text)
alert = {
    "symbol": "EURUSD",
    "timeframe": "M15",
    "prices": np.array([
        1.1000, 1.1005, 1.1010, 1.1008, 1.1015,
        1.1020, 1.1012, 1.1018, 1.1025, 1.1020,
        1.1030, 1.1035, 1.1030, 1.1040, 1.1045,
        1.1040, 1.1050, 1.1055, 1.1050, 1.1060
    ])
}

prices = alert["prices"]

ema50 = ema(prices, 5)
ema200 = ema(prices, 10)
rsi14 = rsi(prices, 5)

trend = "BULLISH" if ema50[-1] > ema200[-1] else "BEARISH"

signal = "HOLD"
if trend == "BULLISH" and rsi14[-1] < 70:
    signal = "BUY"
elif trend == "BEARISH" and rsi14[-1] > 30:
    signal = "SELL"

print("TradingView Analysis")
print("--------------------")
print(f"Symbol: {alert['symbol']}")
print(f"Timeframe: {alert['timeframe']}")
print(f"Trend: {trend}")
print(f"RSI: {rsi14[-1]:.1f}")
print(f"Signal: {signal}")
