import os
import io

from flask import Flask, request, render_template_string
from PIL import Image
import pytesseract

from pair_detector import detect_pair

app = Flask(__name__)

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
    padding:30px;
    border-radius:10px;
    width:90%;
    max-width:400px;
    text-align:center;
}
input, button {
    margin-top:15px;
    width:100%;
}
</style>
</head>
<body>
<div class="box">
    <h2>SignalSnap FX</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Analyze</button>
    </form>
    {% if result %}
        <p><b>Detected Pair:</b> {{ result }}</p>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image)
            result = detect_pair(text)

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
