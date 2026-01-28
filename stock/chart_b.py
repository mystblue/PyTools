import pandas as pd
import mplfinance as mpf

# CSV 読み込み
df = pd.read_csv("fujikura.csv", parse_dates=["Date"], index_col="Date")


# --- ボリンジャーバンド計算（20日・2σ） ---
window = 20
df["MA20"] = df["Close"].rolling(window).mean()
df["STD20"] = df["Close"].rolling(window).std()

df["Upper"] = df["MA20"] + (df["STD20"] * 2)
df["Lower"] = df["MA20"] - (df["STD20"] * 2)


#df_period = df["2024-01-01":"2024-03-31"]
df = df.tail(60)  # 直近60営業日


apds = [
    mpf.make_addplot(df["MA20"], panel=0, width=1, color="blue"),
    mpf.make_addplot(df["Upper"], panel=0, width=1, color="green"),
    mpf.make_addplot(df["Lower"], panel=0, width=1, color="red"),
]








mc = mpf.make_marketcolors(
    up='red',
    down='blue',
    wick={'up':'red', 'down':'blue'},
    volume={'up':'red','down':'blue'}
)

mystyle = mpf.make_mpf_style(
    base_mpf_style='yahoo',
    marketcolors=mc
)

# ローソク足チャート表示
mpf.plot(
    df,
    type="candle",
    volume=False,
    #mav=(5, 25, 75),
    style="yahoo",
    datetime_format="%m-%d",   # ← 日付フォーマット指定
    xrotation=0,               # ← これで横向きになる
    #show_nontrading=True,   # ← 土日も含めて日付が連続
    addplot=apds,
    savefig="candlestick2.png"
)