import re

FOREX_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD",
    "USDCHF", "NZDUSD", "XAUUSD", "XAGUSD",
    "NAS100", "US30", "SPX500", "GER40"
]

def detect_pair(text: str) -> str:
    text = text.upper().replace("/", "")
    for pair in FOREX_PAIRS:
        if pair in text:
            return pair
    return "UNKNOWN"
