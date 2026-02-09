import datetime
import yfinance as yf
import pandas as pd
import ta  # pip install ta

# 1. 監視銘柄リスト
TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "sumco", "screen", "hoya", "rohm", "shinetsu", "tel", "furukawa", "denso", "shionogi", "chugai", "astellas", "nintendo", "capcom", "bandai", "kepco", "tepco", "enos", "mhi", "ihi", "khi", "itochu", "mitsubishi", "mitsui", "olc", "toyota", "nipponsteel", "jfeh", "nyk", "mol", "kilne", "kikkoman", "nipponham", "konami", "squareenix", "suzuki", "subaru", "disco", "renesas", "softbankg", "ntt", "kddi", "softbank", "cyberagent", "rakuten", "zh", "fujitsu", "nec", "omron"]

def fetch_data(ticker):
    data = pd.read_csv("master\\" + ticker + ".csv")
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

    df["STD20"] = df["Close"].rolling(20).std()
    
    df["Upper"] = df["MA20"] + (df["STD20"] * 2)
    df["Lower"] = df["MA20"] - (df["STD20"] * 2)
    df["Lower1"] = df["MA20"] - (df["STD20"])

    return df

def is_buy_signal(df):
    latest = df.iloc[-1]
    prev2 = df.iloc[-2]
    prev3 = df.iloc[-3]
    prev4 = df.iloc[-4]
    
    prev4_cond = prev4["Low"] < prev4["Lower1"]

    latest_cond = latest["Close"] > latest["Open"]
    
    return prev4_cond and latest_cond

def main():
    results = []

    for ticker in TICKERS:
        try:
            df = fetch_data(ticker)
            df = add_indicators(df)

            if len(df) < 25:
                continue

            if is_buy_signal(df):
                latest = df.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "date": latest["Date"],
                    "close": latest["Close"],
                    "rsi": latest["RSI14"],
                    "upper": latest["Upper"],
                })
        except Exception as e:
            print(f"Error for {ticker}: {e}")

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