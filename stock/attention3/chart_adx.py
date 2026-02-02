import numpy as np
import pandas as pd
import mplfinance as mpf

def create_chart(df, n=14):
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))

    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), 
                         np.maximum(df['High'] - df['High'].shift(1), 0), 0)
    df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), 
                         np.maximum(df['Low'].shift(1) - df['Low'], 0), 0)

    df['TRn'] = df['TR'].rolling(n).sum()
    df['+DMn'] = df['+DM'].rolling(n).sum()
    df['-DMn'] = df['-DM'].rolling(n).sum()

    df['+DI'] = 100 * (df['+DMn'] / df['TRn'])
    df['-DI'] = 100 * (df['-DMn'] / df['TRn'])

    df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])) * 100
    df['ADX'] = df['DX'].rolling(n).mean()
    
    #df_period = df["2024-01-01":"2024-03-31"]
    df = df.tail(30)  # 直近60営業日
    #df = df["2025-01-17":"2025-02-01"]
    
    apds = [
        mpf.make_addplot(df['ADX'], panel=1, color='blue', width=1.0),
        mpf.make_addplot(df['+DI'], panel=1, color='green', width=1.0),
        mpf.make_addplot(df['-DI'], panel=1, color='red', width=1.0),
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
        title="Price + ADX / DI",
        savefig="candlestick_adx.png"
    )
    df.to_csv("adx.csv")

if __name__ == '__main__':
    # CSV 読み込み
    df = pd.read_csv("..\\master\\konami.csv", parse_dates=["Date"], index_col="Date")
    create_chart(df)
