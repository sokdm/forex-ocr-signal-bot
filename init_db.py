import sqlite3

db = sqlite3.connect("users.db")

db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    pair TEXT,
    signal TEXT,
    entry REAL,
    tp REAL,
    sl REAL,
    strength TEXT,
    confidence INTEGER,
    explanation TEXT
)
""")

db.commit()
db.close()

print("✅ Database initialized")
