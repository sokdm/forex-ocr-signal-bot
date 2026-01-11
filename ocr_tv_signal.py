import pytesseract
from PIL import Image
import re

# ---------- TP / SL LOGIC ----------
def calculate_tp_sl(price, signal, pair, sl_pips=20, tp_pips=40):
    pip = 0.01 if "JPY" in pair else 0.0001

    if signal == "BUY":
        sl = price - sl_pips * pip
        tp = price + tp_pips * pip
    elif signal == "SELL":
        sl = price + sl_pips * pip
        tp = price - tp_pips * pip
    else:
        return None, None

    return sl, tp


# ---------- PAIR DETECTION ----------
def detect_pair(text):
    pairs = [
        "EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD",
        "NZDUSD","EURJPY","GBPJPY","XAUUSD","XAGUSD"
    ]
    text = text.replace("/", "")
    for p in pairs:
        if p in text:
            return p
    return "UNKNOWN"


# ---------- OCR ----------
img = Image.open("chart.png")
raw_text = pytesseract.image_to_string(img)

print("\nTradingView OCR Signal Bot")
print("--------------------------")
print("\nRAW OCR TEXT\n----------------")
print(raw_text)

# ---------- SIMPLE ANALYSIS ----------
pair = detect_pair(raw_text)
price_match = re.search(r"\d+\.\d+", raw_text)

price = float(price_match.group()) if price_match else None

signal = "HOLD"
if price:
    signal = "BUY"  # placeholder logic (you already know how to improve this)

sl, tp = calculate_tp_sl(price, signal, pair)

print("\nANALYSIS RESULT\n----------------")
print("PAIR:", pair)
print("PRICE:", price)
print("SIGNAL:", signal)

if sl and tp:
    print(f"STOP LOSS: {sl:.5f}")
    print(f"TAKE PROFIT: {tp:.5f}")
