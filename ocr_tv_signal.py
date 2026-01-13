import pytesseract
from PIL import Image
import re
import os

def analyze_image(image_path):
    # TEMPORARY SAFE MODE (Render compatible)
    if os.environ.get("RENDER"):
        return [{
            "pair": "XAUUSD",
            "signal": "BUY",
            "entry": 2310.50,
            "tp": 2325.00,
            "sl": 2295.00,
            "strength": "MEDIUM",
            "confidence": 65,
            "explanation": "OCR disabled on Render (safe mode)",
            "risk": "LOW"
        }]

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        return [{
            "pair": "ERROR",
            "signal": "-",
            "entry": "-",
            "tp": "-",
            "sl": "-",
            "strength": "WEAK",
            "confidence": 0,
            "explanation": f"OCR failed: {str(e)}",
            "risk": "-"
        }]

    text = text.upper()

    pair_match = re.search(r"(EURUSD|GBPUSD|USDJPY|XAUUSD|AUDUSD)", text)
    pair = pair_match.group(1) if pair_match else "UNKNOWN"

    signal = "BUY" if "BUY" in text else "SELL" if "SELL" in text else "-"

    numbers = re.findall(r"\d+\.\d+", text)

    entry = float(numbers[0]) if len(numbers) > 0 else "-"
    tp = float(numbers[1]) if len(numbers) > 1 else "-"
    sl = float(numbers[2]) if len(numbers) > 2 else "-"

    confidence = 60 if signal != "-" else 30
    strength = "STRONG" if confidence >= 70 else "MEDIUM"

    return [{
        "pair": pair,
        "signal": signal,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "strength": strength,
        "confidence": confidence,
        "explanation": "Processed",
        "risk": "-"
    }]
