import yfinance as yf
import pandas as pd
import ta  # pip install ta

# 1. 監視銘柄リスト（例：米国株）
TICKERS = ["NVDA"]

def fetch_data(ticker, period="6mo", interval="1d"):
    #data = yf.download(ticker, period=period, interval=interval, progress=False)
    #data.dropna(inplace=True)
    
    #data = ""
    #with open("fujikura.csv", "r", encoding="utf-8") as f:
    #    data = f.read()
    
    #fujikura = yf.Ticker("5803.T")
    #data = fujikura.history(period="1y")
    #data.dropna(inplace=True)

    data = pd.read_csv("fujikura.csv")

    return data

def add_indicators(df):
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()
    return df

def is_buy_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # ゴールデンクロス（MA5がMA20を上抜け）
    gc = (prev["MA5"] <= prev["MA20"]) and (latest["MA5"] > latest["MA20"])
    print(latest["MA5"])
    print(latest["MA20"])

    # 出来高が平均以上
    vol_ok = latest["Volume"] > latest["VOLUME_MA20"]
    print(latest["Volume"])
    print(latest["VOLUME_MA20"])

    # RSIが50以上（弱すぎない）
    rsi_ok = latest["RSI14"] >= 50
    print(latest["RSI14"])

    # MACDがシグナル上抜け
    macd_ok = (prev["MACD"] <= prev["MACD_SIGNAL"]) and (latest["MACD"] > latest["MACD_SIGNAL"])

    return gc and vol_ok and rsi_ok and macd_ok

def main():
    results = []

    for ticker in TICKERS:
        #try:
            df = fetch_data(ticker)
            df = add_indicators(df)

            if len(df) < 25:
                continue

            if is_buy_signal(df):
                latest = df.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "close": latest["Close"],
                    "rsi": latest["RSI14"],
                    "ma5": latest["MA5"],
                    "ma20": latest["MA20"],
                    "volume": latest["Volume"],
                })
        #except Exception as e:
        #    print(f"Error for {ticker}: {e}")

    if results:
        df_res = pd.DataFrame(results)
        print("今日の買い候補：")
        print(df_res)
        df_res.to_csv("screening_results.csv", index=False)
    else:
        print("今日の条件合致銘柄はなし")

if __name__ == "__main__":
    main()