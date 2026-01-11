from flask import Flask, jsonify
import os

app = Flask(__name__)

# =========================
# RSI CALCULATION
# =========================
def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0  # neutral fallback

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
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)


# =========================
# ANALYSIS LOGIC
# =========================
def analyze_image(image_path=None):
    # TEMP dummy data (replace later with OCR)
    prices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    rsi = calculate_rsi(prices)

    if rsi < 30:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "rsi": rsi,
        "signal": signal
    }


# =========================
# API ROUTE
# =========================
@app.route("/analyze", methods=["GET"])
def analyze():
    result = analyze_image()
    return jsonify(result)


# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
