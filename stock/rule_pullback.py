import datetime
import yfinance as yf
import pandas as pd
import ta  # pip install ta

# 1. 監視銘柄リスト
TICKERS = ["fujikura"]

def fetch_data(ticker):
    df = pd.read_csv("master\\" + ticker + ".csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").set_index("Date")
    return df

# =========================================================
# RSI 計算
# =========================================================
def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    diff = series.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)

    gain = up.ewm(alpha=1/period, adjust=False).mean()
    loss = down.ewm(alpha=1/period, adjust=False).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# =========================================================
# 週足トレンド判定（20MA 上向き & 終値 > 20MA で上昇トレンド）
# =========================================================
def add_weekly_trend(daily: pd.DataFrame) -> pd.DataFrame:
    # 週足にリサンプル
    weekly = daily.resample("W-FRI").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    weekly["MA20"] = weekly["Close"].rolling(20).mean()
    weekly["MA20_slope"] = weekly["MA20"] - weekly["MA20"].shift(1)
    weekly["trend_up"] = (weekly["MA20_slope"] > 0) & (weekly["Close"] > weekly["MA20"])

    # 週足トレンドを日足に forward fill で付与
    trend = weekly[["trend_up"]].reindex(daily.index, method="ffill")
    daily = daily.copy()
    daily["trend_up"] = trend["trend_up"].fillna(False)
    return daily


# =========================================================
# 日足インジケータ（MA, ボリンジャー, RSI）
# =========================================================
def add_daily_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA20_SLOPE"] = df["MA20"].diff()

    # ボリンジャーバンド（20期間）
    period_bb = 20
    df["BB_MID"] = df["Close"].rolling(period_bb).mean()
    df["BB_STD"] = df["Close"].rolling(period_bb).std()
    df["BB_UP"] = df["BB_MID"] + 2 * df["BB_STD"]
    df["BB_LOW"] = df["BB_MID"] - 2 * df["BB_STD"]

    # RSI
    df["RSI"] = calc_rsi(df["Close"], period=14)

    df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()

    return df


# =========================================================
# シグナル生成（順張り＋押し目＋反転確認）
# =========================================================
def generate_long_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 押し目条件（RSI 30〜45 & MA5 or MA10 付近 & 陰線）
    rsi_pullback = (df["RSI"] >= 35) & (df["RSI"] <= 55)

    ma_touch = (
        (abs(df["Close"] - df["MA5"]) / df["Close"] < 0.01) |
        (abs(df["Close"] - df["MA10"]) / df["Close"] < 0.01)
    )

    bearish_candle = df["Close"] < df["Open"]

    prev_close2 = df["Close"].shift(1)
    my = df["Close"] < prev_close2

    pullback = rsi_pullback & ma_touch & bearish_candle & my

    # 反転シグナル（陽線包み足 or RSI 上向き or MA5 上抜け）
    bullish_candle = df["Close"] > df["Open"]
    prev_close = df["Close"].shift(1)
    prev_open = df["Open"].shift(1)

    engulfing = bullish_candle & (df["Close"] > prev_open) & (df["Open"] < prev_close)

    rsi_turn_up = (df["RSI"] > df["RSI"].shift(1))

    ma5_cross_up = (df["Close"] > df["MA5"]) & (df["Close"].shift(1) <= df["MA5"].shift(1))

    vol_ok = df["Volume"] > df["VOLUME_MA20"]

    reversal = engulfing | rsi_turn_up | ma5_cross_up | vol_ok

    # 週足トレンドが上昇 & 押し目後の反転でロングエントリー
    df["long_entry"] = df["trend_up"] & pullback.shift(1) & reversal

    return df

def main():
    results = []

    for ticker in TICKERS:
        #try:
            df = fetch_data(ticker)
            df = add_weekly_trend(df)
            df = add_daily_indicators(df)
            df = generate_long_signals(df)

            if len(df) < 25:
                continue

            if df.iloc[-1]["long_entry"]:
                latest = df.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "date": latest["Date"],
                    "close": latest["Close"],
                    "rsi": latest["RSI14"],
                    "ma5": latest["MA5"],
                    "ma20": latest["MA20"],
                    "pref_date": df.iloc[-2]["Date"],
                    "PREV_ma5": df.iloc[-2]["MA5"],
                    "PREV_ma20": df.iloc[-2]["MA20"],
                    "volume": latest["Volume"],
                })
        #except Exception as e:
        #    print(f"Error for {ticker}: {e}")

    if results:
        df_res = pd.DataFrame(results)
        print("今日の買い候補：")
        print(df_res)
        
        now = datetime.datetime.now()
        date_str = now.strftime('%Y%m%d')
        df_res.to_csv("screening_results_" + date_str + ".csv", index=False)
    else:
        print("今日の条件合致銘柄はなし")

if __name__ == "__main__":
    main()