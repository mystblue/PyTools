import pandas as pd
import mplfinance as mpf

def create_chart(df):
    # ローソク足チャート表示
    mpf.plot(
        df,
        type="candle",
        volume=False,
        style="yahoo",
        datetime_format="%H-%M",
        xrotation=0,               # ← これで横向きになる
        savefig="candlestick_1h.png"
    )

if __name__ == '__main__':
    # CSV 読み込み
    df = pd.read_csv("mol_1h.csv", parse_dates=["Datetime"], index_col="Datetime")
    create_chart(df)
