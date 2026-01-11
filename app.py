from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Forex OCR Signal API is LIVE"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    if "prices" not in data:
        return jsonify({"error": "prices array missing"}), 400

    prices = data["prices"]

    if not isinstance(prices, list):
        return jsonify({"error": "prices must be a list"}), 400

    if len(prices) < 14:
        return jsonify({"error": "Not enough prices (minimum 14)"}), 400

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

    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    if rsi > 70:
        signal = "SELL"
    elif rsi < 30:
        signal = "BUY"
    else:
        signal = "HOLD"

    return jsonify({
        "status": "success",
        "pair": "EURUSD",
        "timeframe": "15m",
        "rsi": round(rsi, 2),
        "signal": signal
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
