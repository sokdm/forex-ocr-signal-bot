import re

PAIRS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"]

def analyze_ocr_text(text):
    text = text.upper().replace("/", "").replace(" ", "")

    results = []

    # -------- Pair detection --------
    pair = "UNKNOWN"
    for p in PAIRS:
        if p in text:
            pair = p
            break

    # -------- Signal detection --------
    if "BUY" in text:
        signal = "BUY"
    elif "SELL" in text:
        signal = "SELL"
    else:
        signal = "HOLD"

    # -------- Price extraction --------
    numbers = re.findall(r"\d+\.\d+", text)
    entry = tp = sl = "-"

    if len(numbers) >= 3:
        entry = float(numbers[0])
        tp = float(numbers[1])
        sl = float(numbers[2])

    # -------- Strength logic --------
    strength_score = 0
    explanation = []

    if signal in ["BUY", "SELL"]:
        strength_score += 30
        explanation.append("Clear trade direction detected")

    if entry != "-" and tp != "-" and sl != "-":
        strength_score += 30
        explanation.append("Valid entry, TP and SL found")

    rr = None
    if entry != "-" and tp != "-" and sl != "-":
        try:
            risk = abs(entry - sl)
            reward = abs(tp - entry)
            rr = round(reward / risk, 2)
            if rr >= 2:
                strength_score += 25
                explanation.append(f"Good risk-reward ratio ({rr}:1)")
            else:
                explanation.append(f"Weak risk-reward ratio ({rr}:1)")
        except:
            pass

    if pair != "UNKNOWN":
        strength_score += 15
        explanation.append("Currency pair clearly identified")

    # -------- Confidence calculation --------
    confidence = min(95, strength_score)

    if confidence >= 80:
        strength = "STRONG"
    elif confidence >= 60:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    # -------- Risk management --------
    if rr and rr >= 2:
        risk_note = "Risk only 1–2% of account"
    else:
        risk_note = "Reduce lot size due to low RR"

    explanation_text = "; ".join(explanation)

    # -------- Final filter --------
    if signal == "HOLD" or pair == "UNKNOWN":
        return []

    results.append({
        "pair": pair,
        "signal": signal,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "strength": strength,
        "confidence": confidence,
        "explanation": explanation_text,
        "risk": risk_note
    })

    return results
