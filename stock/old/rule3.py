import yfinance as yf
import pandas as pd
import ta

# ===== 監視銘柄 =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]

# ===== データ取得 =====
def fetch_data(ticker, period="6mo", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    df.dropna(inplace=True)
    return df

# ===== テクニカル指標 =====
def add_indicators(df):
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["VOL_MA20"] = df["Volume"].rolling(window=20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    return df.dropna()

# ===== ルール①：20MAブレイク =====
def rule1(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    cond1 = (prev["Close"] <= prev["MA20"]) and (latest["Close"] > latest["MA20"])
    cond2 = latest["MA20"] > prev["MA20"]
    cond3 = latest["Volume"] >= latest["VOL_MA20"]

    return cond1 and cond2 and cond3

# ===== ルール②：5MA × 20MA ゴールデンクロス =====
def rule2(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    cond1 = (prev["MA5"] <= prev["MA20"]) and (latest["MA5"] > latest["MA20"])
    cond2 = latest["MA20"] >= prev["MA20"]  # 横ばい〜上向き
    cond3 = latest["RSI14"] >= 50

    return cond1 and cond2 and cond3

# ===== ルール③：MACDシグナル上抜け =====
def rule3(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    cond1 = (prev["MACD"] <= prev["MACD_SIGNAL"]) and (latest["MACD"] > latest["MACD_SIGNAL"])
    cond2 = latest["Close"] > latest["MA20"]
    cond3 = latest["Volume"] >= latest["VOL_MA20"]

    return cond1 and cond2 and cond3

# ===== メイン処理 =====
def main():
    results = []

    for ticker in TICKERS:
        try:
            df = fetch_data(ticker)
            df = add_indicators(df)

            r1 = rule1(df)
            r2 = rule2(df)
            r3 = rule3(df)

            if r1 or r2 or r3:
                latest = df.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "close": round(latest["Close"], 2),
                    "rule1": r1,
                    "rule2": r2,
                    "rule3": r3
                })

        except Exception as e:
            print(f"[{ticker}] Error: {e}")

    if results:
        df_res = pd.DataFrame(results)
        print("=== 今日の買いシグナル銘柄（ルール1〜3） ===")
        print(df_res)
        df_res.to_csv("trend_rules_signals.csv", index=False)
    else:
        print("今日はどのルールにも合致した銘柄なし")

if __name__ == "__main__":
    main()