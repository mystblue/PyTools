import pandas as pd
import mplfinance as mpf

# CSV 読み込み
df = pd.read_csv("ibiden.csv", parse_dates=["Date"], index_col="Date")



# --- MACD 計算 ---
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
df["MACD"] = df["EMA12"] - df["EMA26"]
df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["Hist"] = df["MACD"] - df["Signal"]



#df_period = df["2024-01-01":"2024-03-31"]
df = df.tail(60)  # 直近60営業日


apds = [
    mpf.make_addplot(df["MACD"], panel=1, width=1, color="blue"),
    mpf.make_addplot(df["Signal"], panel=1, width=1, color="red"),
    mpf.make_addplot(df["Hist"], panel=1, width=1, type="bar", color="gray", alpha=0.5)
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
    savefig="candlestick3.png"
)