import re

def analyze_text(raw_text):
    pair = "UNKNOWN"
    if "EURUSD" in raw_text:
        pair = "EURUSD"
    elif "GBPUSD" in raw_text:
        pair = "GBPUSD"

    price_match = re.search(r"\d+\.\d+", raw_text)
    price = float(price_match.group()) if price_match else None

    rsi = 72.5  # placeholder (later auto-calculated)

    if rsi > 70:
        signal = "SELL"
        strength = "STRONG"
    elif rsi < 30:
        signal = "BUY"
        strength = "STRONG"
    else:
        signal = "HOLD"
        strength = "WEAK"

    sl = round(price + 0.002, 3) if signal == "SELL" else round(price - 0.002, 3)
    tp = round(price - 0.003, 3) if signal == "SELL" else round(price + 0.003, 3)

    return {
        "pair": pair,
        "entry": price,
        "rsi": rsi,
        "signal": signal,
        "strength": strength,
        "sl": sl,
        "tp": tp
    }
