import numpy as np
import pandas as pd
import mplfinance as mpf

def create_chart(df, n=14):
    # True Range の計算
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = (df['High'] - df['Close'].shift(1)).abs()
    df['L-PC'] = (df['Low'] - df['Close'].shift(1)).abs()

    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    # ATR（単純移動平均）
    df['ATR'] = df['TR'].rolling(window=14).mean()

    # EMA ATR
    df['EMAATR'] = df['TR'].ewm(alpha=1/14, adjust=False).mean()

    #df_period = df["2024-01-01":"2024-03-31"]
    df = df.tail(30)  # 直近60営業日
    #df = df["2025-01-17":"2025-02-01"]
    
    apds = [
        mpf.make_addplot(df['EMAATR'], panel=1, color='blue', width=1.0, label="ATR"),
        #mpf.make_addplot(df['TR'], panel=1, color='green', width=1.0, label="TR"),
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
        #figsize=(14,8),
        title="Price + ATR",
        savefig="candlestick_atr.png"
    )
    df.to_csv("adx.csv")

if __name__ == '__main__':
    # CSV 読み込み
    df = pd.read_csv("..\\master\\appier.csv", parse_dates=["Date"], index_col="Date")
    create_chart(df)
