import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv")
    return data

def main():
    df = fetch_data()
    print(df["Open"].mean())
    print(df["Close"].mean())
    print(df)
    df["MA5"] = df["Close"].rolling(window=5).mean()
    print(df)
    df = df.dropna()
    print(df)

if __name__ == "__main__":
    main()