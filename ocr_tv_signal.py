import pytesseract
from PIL import Image
import re

print("TradingView OCR Signal Bot")
print("--------------------------")

# Load image
img = Image.open("chart.png")

# Extract text
text = pytesseract.image_to_string(img)

print("\nRAW OCR TEXT")
print("----------------")
print(text)

# Extract RSI value
rsi_match = re.search(r'RSI[^0-9]*([0-9]+\.?[0-9]*)', text)
rsi_value = float(rsi_match.group(1)) if rsi_match else None

signal = "HOLD"
if rsi_value is not None:
    if rsi_value < 30:
        signal = "BUY"
    elif rsi_value > 70:
        signal = "SELL"

print("\nANALYSIS RESULT")
print("----------------")
print(f"RSI: {rsi_value}")
print(f"SIGNAL: {signal}")
