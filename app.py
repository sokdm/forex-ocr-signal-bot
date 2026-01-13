from flask import Flask, render_template, request, redirect, session, url_for
from auth import login_required
from werkzeug.utils import secure_filename
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================
# DATABASE
# ======================
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return redirect("/login")

# ======================
# SIGNUP
# ======================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )
            db.commit()
        except:
            return "Email already exists"

        return redirect("/login")

    return render_template("signup.html")
# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")
# ======================
# DASHBOARD (HISTORY)
# ======================
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    trades = db.execute(
        "SELECT pair, signal, entry, tp, sl, strength, confidence, explanation "
        "FROM trades WHERE user_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    db.close()

    return render_template("dashboard.html", trades=trades)

# ======================
# UPLOAD + ANALYZE
# ======================
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        image = request.files["image"]
        filename = secure_filename(image.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(path)

        # ===== ANALYSIS (PLACEHOLDER, OCR LATER) =====
        result = {
            "pair": "EURUSD",
            "signal": "SELL",
            "entry": 1.166,
            "tp": 1.163,
            "sl": 1.168,
            "strength": "STRONG",
            "confidence": 85,
            "explanation": "RSI overbought, bearish momentum confirmed. RR 1:2"
        }

        return render_template("result.html", result=result)

    return render_template("upload.html")

# ======================
# SAVE RESULT → DASHBOARD
# ======================
@app.route("/save_trade", methods=["POST"])
@login_required
def save_trade():
    db = get_db()
    db.execute("""
    INSERT INTO trades
    (user_id, pair, signal, entry, tp, sl, strength, confidence, explanation)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        request.form["pair"],
        request.form["signal"],
        request.form["entry"],
        request.form["tp"],
        request.form["sl"],
        request.form["strength"],
        request.form["confidence"],
        request.form["explanation"]
    ))
    db.commit()
    db.close()

    return redirect("/dashboard")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
