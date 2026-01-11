from flask import Flask, jsonify
import os

# import your function
from smart_rsi import calculate_rsi

app = Flask(__name__)

def analyze_image(image_path=None):
    dummy_prices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    rsi = calculate_rsi(dummy_prices)

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

@app.route("/")
def home():
    return jsonify({
        "status": "OK",
        "message": "Forex OCR Signal Bot is running"
    })

@app.route("/test")
def test():
    return jsonify(analyze_image())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
