from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    # ✅ MOCK RESULT (replace later with real OCR/RSI logic)
    result = {
        "pair": "UNKNOWN",
        "signal": "BUY",
        "price": "0.24",
        "stop_loss": "0.238",
        "take_profit": "0.244"
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
