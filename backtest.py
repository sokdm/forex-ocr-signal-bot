import numpy as np
import csv
from indicators import ema, rsi

# Load CSV close prices
prices = []

with open("eurusd_m15.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        prices.append(float(row["close"]))

prices = np.array(prices)

ema50 = ema(prices, 5)
ema200 = ema(prices, 10)
rsi14 = rsi(prices, 5)

balance = 100.0
lot = 0.01
position = None
entry_price = 0.0
wins = 0
losses = 0

# Risk management
stop_loss = 0.0020
take_profit = 0.0040

print("Running CSV Backtest...")

for i in range(len(prices)):
    price = prices[i]

    if position is None:
        if ema50[i] > ema200[i] and rsi14[i] < 70:
            position = "BUY"
            entry_price = price
            sl = entry_price - stop_loss
            tp = entry_price + take_profit

    else:
        if price <= sl or price >= tp:
            profit = (price - entry_price) * 10000 * lot
            balance += profit

            if profit > 0:
                wins += 1
            else:
                losses += 1

            position = None

total_trades = wins + losses
win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

print("\nBacktest Results")
print("----------------")
print(f"Final Balance: ${balance:.2f}")
print(f"Trades Taken: {total_trades}")
print(f"Wins: {wins}")
print(f"Losses: {losses}")
print(f"Win Rate: {win_rate:.1f}%")
