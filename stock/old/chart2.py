import pandas as pd
import matplotlib.pyplot as plt

# CSV 読み込み
df = pd.read_csv("fujikura.csv", parse_dates=["Date"])
df.set_index("Date", inplace=True)

# チャート描画
plt.figure(figsize=(12, 6))
plt.plot(df["Close"], label="Close Price")
plt.title("Stock Price")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.legend()

# 画像として保存
plt.savefig("stock_chart.png", dpi=200, bbox_inches="tight")

# 画面にも表示したい場合
plt.show()