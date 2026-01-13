import pytesseract
from PIL import Image
import re

def analyze_image(image_path):
    # ---------- OCR ----------
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    text = text.upper()

    # ---------- PAIR ----------
    pair_match = re.search(r"(EURUSD|GBPUSD|USDJPY|XAUUSD|AUDUSD)", text)
    pair = pair_match.group(1) if pair_match else "UNKNOWN"

    # ---------- SIGNAL ----------
    signal = "BUY" if "BUY" in text else "SELL" if "SELL" in text else "-"

    # ---------- NUMBERS ----------
    numbers = re.findall(r"\d+\.\d+", text)

    entry = float(numbers[0]) if len(numbers) > 0 else "-"
    tp = float(numbers[1]) if len(numbers) > 1 else "-"
    sl = float(numbers[2]) if len(numbers) > 2 else "-"

    # ---------- STRENGTH ----------
    strength_score = 0
    explanation = []

    if signal in ["BUY", "SELL"]:
        strength_score += 30
        explanation.append("Clear trade direction")

    if entry != "-" and tp != "-" and sl != "-":
        strength_score += 30
        explanation.append("Valid entry, TP and SL")

    rr = None
    if entry != "-" and tp != "-" and sl != "-":
        try:
            risk = abs(entry - sl)
            reward = abs(tp - entry)
            rr = round(reward / risk, 2)
            if rr >= 2:
                strength_score += 25
                explanation.append(f"Good RR {rr}")
        except:
            pass

    # ---------- CONFIDENCE ----------
    confidence = min(95, strength_score)

    strength = "STRONG" if confidence >= 70 else "MEDIUM" if confidence >= 50 else "WEAK"

    return [{
        "pair": pair,
        "signal": signal,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "strength": strength,
        "confidence": confidence,
        "explanation": ", ".join(explanation),
        "risk": f"RR {rr}" if rr else "RR unknown"
    }]
