def calculate_rsi(prices, period=14):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period if sum(losses[-period:]) != 0 else 1

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)


def smart_rsi_signal(prices):
    rsi = calculate_rsi(prices)

    if rsi < 30:
        return {
            "signal": "BUY",
            "strength": "STRONG",
            "rsi": rsi
        }

    if rsi > 70:
        return {
            "signal": "SELL",
            "strength": "STRONG",
            "rsi": rsi
        }

    return {
        "signal": "WAIT",
        "strength": "WEAK",
        "rsi": rsi
    }
