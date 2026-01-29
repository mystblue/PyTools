# 短期EMA（12日）の全計算過程を表示
prices = [100, 101, 102, 101, 103, 104, 105, 106, 107, 108, 109, 110, 111]
n = 9
alpha = 2 / (n + 1)  # 平滑化係数

print(f"期間: {n}日, α = {alpha:.4f}\n")

# 初期EMA（SMA）
initial_ema = sum(prices[:n]) / n
print(f"初期EMA（SMA）: {initial_ema:.2f}\n")

ema = initial_ema

# 各日の計算過程を表示
for i in range(n, len(prices)):
    today_price = prices[i]
    prev_ema = ema
    ema = (today_price * alpha) + (prev_ema * (1 - alpha))
    print(f"Day {i+1}: Price={today_price}, "
          f"Prev EMA={prev_ema:.2f}, "
          f"Weight Price={alpha:.4f}, "
          f"Weight EMA={(1-alpha):.4f}, "
          f"New EMA={ema:.2f}")
