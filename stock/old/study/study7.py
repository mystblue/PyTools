import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv")
    return data

def main():
    df = fetch_data()
    print(df)
    df["MA5"] = df["Close"].rolling(5).mean()
    df = df.dropna()
    print(df)
    df["MA25_SLOPE"] = df["MA5"].diff()
    print(df)
    
if __name__ == "__main__":
    main()