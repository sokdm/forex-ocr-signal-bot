from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_rsi(prices, period=14):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    prices = data.get("prices")

    if not prices or len(prices) < 15:
        return jsonify({"error": "Not enough prices"}), 400

    rsi = calculate_rsi(prices)
    entry = prices[-1]

    if rsi > 70:
        signal = "SELL"
        tp = round(entry - 0.003, 3)
        sl = round(entry + 0.002, 3)
    elif rsi < 30:
        signal = "BUY"
        tp = round(entry + 0.003, 3)
        sl = round(entry - 0.002, 3)
    else:
        signal = "HOLD"
        tp = sl = entry

    strength = "STRONG" if rsi > 75 or rsi < 25 else "WEAK"

    return jsonify({
        "signal": signal,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "rsi": rsi,
        "strength": strength
    })


@app.route("/")
def home():
    return "Forex OCR Signal API is LIVE"


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
