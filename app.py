from flask import Flask, request, render_template_string
from PIL import Image
import pytesseract
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TradingView Signal Bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; padding: 20px; background: #111; color: #eee; }
        button { padding: 10px; font-size: 16px; }
        input { margin-bottom: 10px; }
        .box { background: #222; padding: 15px; border-radius: 8px; }
    </style>
</head>
<body>

<h2>📈 TradingView Signal Bot</h2>

<form method="POST" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*" required><br>
    <button type="submit">Analyze</button>
</form>

{% if result %}
<div class="box">
<pre>{{ result }}</pre>
</div>
{% endif %}

</body>
</html>
"""

def extract_rsi(text):
    match = re.search(r'RSI[^0-9]*([0-9]+\\.?[0-9]*)', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def analyze_rsi(rsi, price=1.0):
    if rsi is None:
        return "RSI not detected"

    if rsi < 30:
        signal = "BUY"
        sl = price - 0.0020
        tp = price + 0.0040
    elif rsi > 70:
        signal = "SELL"
        sl = price + 0.0020
        tp = price - 0.0040
    else:
        signal = "HOLD"
        sl = tp = None

    return f"""RSI: {rsi}
Signal: {signal}
Stop Loss: {sl if sl else 'N/A'}
Take Profit: {tp if tp else 'N/A'}"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            rsi = extract_rsi(text)
            result = analyze_rsi(rsi)

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
