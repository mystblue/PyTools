import yfinance as yf
import pandas as pd
import ta

# ===== 監視銘柄 =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]

# ===== 日足データ取得 =====
def fetch_daily(ticker, period="6mo"):
    df = yf.download(ticker, period=period, interval="1d", progress=False)
    df.dropna(inplace=True)
    return df

# ===== 週足データ取得 =====
def fetch_weekly(ticker, period="2y"):
    df = yf.download(ticker, period=period, interval="1wk", progress=False)
    df.dropna(inplace=True)
    return df

# ===== 日足テクニカル =====
def add_daily_indicators(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["VOL_MA20"] = df["Volume"].rolling(20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], 14).rsi()
    return df.dropna()

# ===== 週足テクニカル =====
def add_weekly_indicators(df):
    df["W_MA20"] = df["Close"].rolling(20).mean()
    return df.dropna()

# ===== 改善後ルール：買い判定 =====
def is_buy_signal(daily, weekly):
    latest = daily.iloc[-1]
    prev = daily.iloc[-2]

    # 1. 20MAブレイク
    cond_break = (prev["Close"] <= prev["MA20"]) and (latest["Close"] > latest["MA20"])

    # 2. 20MA上向き
    cond_ma_up = latest["MA20"] > prev["MA20"]

    # 3. RSI >= 50
    cond_rsi = latest["RSI14"] >= 50

    # 4. 出来高 >= 20日平均
    cond_vol = latest["Volume"] >= latest["VOL_MA20"]

    # 5. 週足20MAの上
    w_latest = weekly.iloc[-1]
    cond_week = w_latest["Close"] > w_latest["W_MA20"]

    return all([cond_break, cond_ma_up, cond_rsi, cond_vol, cond_week])

# ===== メイン処理 =====
def main():
    results = []

    for ticker in TICKERS:
        try:
            # 日足
            daily = fetch_daily(ticker)
            daily = add_daily_indicators(daily)

            # 週足
            weekly = fetch_weekly(ticker)
            weekly = add_weekly_indicators(weekly)

            # 判定
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

    # 結果出力
    if results:
        df_res = pd.DataFrame(results)
        print("=== 今日の改善後ルール・買いシグナル銘柄 ===")
        print(df_res)
        df_res.to_csv("improved_trend_signals.csv", index=False)
    else:
        print("今日は条件に合致した銘柄なし")

if __name__ == "__main__":
    main()