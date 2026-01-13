from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import uuid
from ocr_tv_signal import analyze_image

app = Flask(__name__)
app.secret_key = "super-secret-key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("username", "guest")
        return redirect("/dashboard")

    return render_template_string("""
    <h2>Login</h2>
    <form method="post">
        <input name="username" placeholder="Username" required>
        <button type="submit">Login</button>
    </form>
    """)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template_string("""
    <h2>Welcome {{user}}</h2>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Analyze</button>
    </form>

    {% if result %}
        <hr>
        <h3>Result</h3>
        <pre>{{ result }}</pre>
    {% endif %}
    """, user=session["user"], result=session.get("result"))

# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect("/")

    file = request.files.get("image")
    if not file:
        return redirect("/dashboard")

    # UNIQUE filename every upload (FIXES SAME-RESULT BUG)
    filename = f"{uuid.uuid4()}.png"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    result = analyze_image(path)

    session["result"] = result

    return redirect("/dashboard")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
