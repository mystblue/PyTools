import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timedelta

# ===== 監視銘柄リスト =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]

# ===== データ取得 =====
def fetch_daily_data(ticker, period="6mo", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    df.dropna(inplace=True)
    return df

def fetch_weekly_data(ticker, period="2y"):
    # 週足は1週間足で取得
    df = yf.download(ticker, period=period, interval="1wk", progress=False)
    df.dropna(inplace=True)
    return df

# ===== テクニカル指標付与（日足） =====
def add_daily_indicators(df):
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    df["VOL_MA20"] = df["Volume"].rolling(window=20).mean()
    return df

# ===== テクニカル指標付与（週足） =====
def add_weekly_indicators(df):
    df["W_MA20"] = df["Close"].rolling(window=20).mean()
    return df

# ===== 健二式トレンドフォロー：買い判定 =====
def is_buy_signal(daily_df, weekly_df):
    # 日足：最新と1本前
    latest = daily_df.iloc[-1]
    prev = daily_df.iloc[-2]

    # 1. 終値が20MAを上抜け
    cond_break_ma20 = (prev["Close"] <= prev["MA20"]) and (latest["Close"] > latest["MA20"])

    # 2. 20MAが上向き（今日のMA20 > 昨日のMA20）
    cond_ma20_up = latest["MA20"] > prev["MA20"]

    # 3. RSI >= 50
    cond_rsi = latest["RSI14"] >= 50

    # 4. 出来高 >= 20日平均
    cond_vol = latest["Volume"] >= latest["VOL_MA20"]

    # 5. 週足でも20MAの上（直近週足終値 > 週足20MA）
    w_latest = weekly_df.iloc[-1]
    cond_week_trend = (w_latest["Close"] > w_latest["W_MA20"])

    return all([cond_break_ma20, cond_ma20_up, cond_rsi, cond_vol, cond_week_trend])

def main():
    results = []

    for ticker in TICKERS:
        try:
            # 日足データ
            daily = fetch_daily_data(ticker)
            if len(daily) < 25:
                continue
            daily = add_daily_indicators(daily)
            daily = daily.dropna()

            # 週足データ
            weekly = fetch_weekly_data(ticker)
            if len(weekly) < 25:
                continue
            weekly = add_weekly_indicators(weekly)
            weekly = weekly.dropna()

            if len(daily) < 22 or len(weekly) < 21:
                continue

            if is_buy_signal(daily, weekly):
                latest = daily.iloc[-1]
                w_latest = weekly.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "date": latest.name.strftime("%Y-%m-%d"),
                    "close": round(latest["Close"], 2),
                    "ma20": round(latest["MA20"], 2),
                    "rsi14": round(latest["RSI14"], 1),
                    "volume": int(latest["Volume"]),
                    "vol_ma20": int(latest["VOL_MA20"]),
                    "weekly_close": round(w_latest["Close"], 2),
                    "weekly_ma20": round(w_latest["W_MA20"], 2),
                })

        except Exception as e:
            print(f"[{ticker}] Error: {e}")

    if results:
        df_res = pd.DataFrame(results)
        print("=== 今日のトレンドフォロー買いシグナル銘柄 ===")
        print(df_res)
        df_res.to_csv("trend_signals.csv", index=False)
    else:
        print("今日は条件に合致した銘柄なし")

if __name__ == "__main__":
    main()