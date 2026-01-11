from flask import Flask, request, render_template_string

app = Flask(__name__)

UPLOAD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SignalSnap FX</title>
</head>
<body>
    <h2>Upload chart screenshot</h2>
    <form method="POST" action="/analyze" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <br><br>
        <button type="submit">Analyze</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(UPLOAD_PAGE)

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("image")
    if not file:
        return "No image uploaded"

    return "Image received ✅ (analysis coming next)"

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
