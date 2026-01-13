from flask import Flask, render_template, request
import os
from ocr_tv_signal import analyze_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    result = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            result = analyze_image(path)[0]

    return f"""
    <h2>Upload Trading Screenshot</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Analyze</button>
    </form>

    {f'''
    <h3>Result</h3>
    Pair: {result["pair"]}<br>
    Signal: {result["signal"]}<br>
    Entry: {result["entry"]}<br>
    TP: {result["tp"]}<br>
    SL: {result["sl"]}<br>
    Strength: {result["strength"]}<br>
    Confidence: {result["confidence"]}%<br>
    Explanation: {result["explanation"]}<br>
    Risk: {result["risk"]}
    ''' if result else ""}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
