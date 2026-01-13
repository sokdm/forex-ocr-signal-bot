import easyocr
import re
from PIL import Image

# Initialize once (VERY IMPORTANT)
reader = easyocr.Reader(['en'], gpu=False)

def analyze_image(image_path):
    try:
        result = reader.readtext(image_path, detail=0)
        text = " ".join(result).upper()
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

    # ---- PAIR ----
    pair_match = re.search(r"(EURUSD|GBPUSD|USDJPY|XAUUSD|AUDUSD)", text)
    pair = pair_match.group(1) if pair_match else "UNKNOWN"

    # ---- SIGNAL ----
    signal = "BUY" if "BUY" in text else "SELL" if "SELL" in text else "-"

    # ---- PRICES ----
    numbers = re.findall(r"\d+\.\d+", text)
    entry = float(numbers[0]) if len(numbers) > 0 else "-"
    tp = float(numbers[1]) if len(numbers) > 1 else "-"
    sl = float(numbers[2]) if len(numbers) > 2 else "-"

    # ---- CONFIDENCE ----
    confidence = 70 if signal != "-" and entry != "-" else 40
    strength = "STRONG" if confidence >= 70 else "MEDIUM"

    return [{
        "pair": pair,
        "signal": signal,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "strength": strength,
        "confidence": confidence,
        "explanation": "Image analyzed successfully",
        "risk": "-"
    }]
