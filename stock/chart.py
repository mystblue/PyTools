import pandas as pd
import mplfinance as mpf

# CSV 読み込み
df = pd.read_csv("fujikura.csv", parse_dates=["Date"], index_col="Date")

#df_period = df["2024-01-01":"2024-03-31"]
df = df.tail(60)  # 直近60営業日

# ローソク足チャート表示
mpf.plot(
    df,
    type="candle",
    volume=True,
    mav=(5, 25),
    style="yahoo"
)