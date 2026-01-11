import numpy as np

def ema(prices, period):
    prices = np.array(prices, dtype=float)
    ema_values = []
    k = 2 / (period + 1)
    ema_values.append(prices[0])
    for price in prices[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))
    return np.array(ema_values)

def rsi(prices, period=14):
    prices = np.array(prices, dtype=float)
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100 - 100 / (1 + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        gain = max(delta, 0)
        loss = -min(delta, 0)
        up = (up * (period - 1) + gain) / period
        down = (down * (period - 1) + loss) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100 - 100 / (1 + rs)
    return rsi

print("Indicators ready ✅")
