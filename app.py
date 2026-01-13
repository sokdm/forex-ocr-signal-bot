from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- ROOT ----------
@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------- SIGNUP ----------
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
            return "User already exists"

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------- LOGIN ----------
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
            return redirect(url_for("dashboard"))

        return "Invalid credentials"

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    trades = db.execute(
        "SELECT * FROM trades WHERE user_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()

    return render_template("dashboard.html", trades=trades)


# ---------- IMAGE UPLOAD ----------
@app.route("/upload", methods=["POST"])
def upload():
    if "user_id" not in session:
        return redirect(url_for("login"))

    image = request.files["image"]
    filename = image.filename
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(path)

    # ----- FAKE ANALYSIS (FOR NOW) -----
    pair = "EURUSD"
    entry = 1.166
    tp = 1.163
    sl = 1.168
    rsi = 72.5

    if rsi > 70:
        signal = "SELL"
        strength = "STRONG"
        confidence = 85
        explanation = "RSI above 70 indicates overbought market"
    else:
        signal = "BUY"
        strength = "WEAK"
        confidence = 40
        explanation = "No strong confirmation"

    db = get_db()
    db.execute("""
        INSERT INTO trades
        (user_id, pair, signal, entry, tp, sl, strength, confidence, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_id"], pair, signal,
        entry, tp, sl,
        strength, confidence, explanation
    ))
    db.commit()

    return redirect(url_for("dashboard"))


# ---------- RUN LOCAL ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
