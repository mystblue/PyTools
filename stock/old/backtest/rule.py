import yfinance as yf
import pandas as pd
import ta  # pip install ta

# 1. 監視銘柄リスト
TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "sumco", "screen", "hoya", "rohm", "shinetsu", "tel", "furukawa", "denso", "shionogi", "chugai", "astellas", "nintendo", "capcom", "bandai", "kepco", "tepco", "enos", "mhi", "ihi", "khi", "itochu", "mitsubishi", "mitsui", "olc", "toyota", "nipponsteel", "jfeh", "nyk", "mol", "kilne", "kikkoman", "nipponham", "konami", "squareenix", "suzuki", "subaru", "disco", "renesas", "softbankg", "ntt", "kddi", "softbank", "cyberagent", "rakuten", "zh", "fujitsu", "nec", "omron"]

def fetch_data(ticker):
    data = pd.read_csv(ticker + "_10y.csv")

    return data

# ===== テクニカル付与 =====
def add_indicators(df):
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()
    
    # 25 日線が上向きを追加
    df["MA25"] = df["Close"].rolling(25).mean()
    df["MA25_SLOPE"] = df["MA25"].diff()

    # 75 日線が上向きを追加
    df["MA75"] = df["Close"].rolling(75).mean()
    df["MA75_SLOPE"] = df["MA75"].diff()

    return df

def is_buy_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # ゴールデンクロス（MA5がMA20を上抜け）
    #gc = (prev["MA5"] <= prev["MA20"]) and (latest["MA5"] > latest["MA20"])

    # 出来高が平均以上
    vol_ok = latest["Volume"] > latest["VOLUME_MA20"]

    # RSIが50以上（弱すぎない）
    #rsi_ok = latest["RSI14"] >= 50
    rsi_ok = latest["RSI14"] >= 45

    # MACDがシグナル上抜け
    macd_ok = (prev["MACD"] <= prev["MACD_SIGNAL"]) and (latest["MACD"] > latest["MACD_SIGNAL"])

    cond6 = latest["MA25_SLOPE"] > 0

    cond75 = latest["MA75_SLOPE"] > 0

    #return gc and vol_ok and rsi_ok and macd_ok
    #return rsi_ok and cond6 and cond75 and macd_ok
    return vol_ok and rsi_ok and macd_ok and cond6 and cond75

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