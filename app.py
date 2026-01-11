from flask import Flask, request, render_template_string
from PIL import Image
import pytesseract
import io

from pair_detector import detect_pair

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SignalSnap FX</title>
<style>
body {
    background:#0b1220;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
    margin-top:80px;
}
.box {
    background:#111a2e;
    padding:25px;
    border-radius:12px;
    width:320px;
    text-align:center;
}
button {
    background:#1ed760;
    border:none;
    padding:10px;
    width:100%;
    border-radius:6px;
    font-weight:bold;
}
</style>
</head>
<body>
<div class="box">
<h2>📊 SignalSnap FX</h2>

<form method="post" enctype="multipart/form-data">
<input type="file" name="image" required><br><br>
<button type="submit">Analyze Screenshot</button>
</form>

{% if result %}
<hr>
<p><b>Pair:</b> {{ result.pair }}</p>
<p><b>Signal:</b> {{ result.signal }}</p>
<p><b>Price:</b> {{ result.price }}</p>
<p><b>Stop Loss:</b> {{ result.sl }}</p>
<p><b>Take Profit:</b> {{ result.tp }}</p>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]
        image = Image.open(io.BytesIO(file.read()))

        text = pytesseract.image_to_string(image)
        pair = detect_pair(text)

        result = {
            "pair": pair,
            "signal": "BUY",
            "price": "0.24",
            "sl": "0.238",
            "tp": "0.244"
        }

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
