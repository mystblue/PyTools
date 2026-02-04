import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    df = pd.read_csv("fujikura.csv")
    df = df.set_index("Date")
    return df

def main():
    df = fetch_data()
    print(df["Close"])
    df2 = df.copy()
    print(df2["Close"].shift(1))
    df3 = df.copy()
    print(df)
    print(df.shift(1))
    
if __name__ == "__main__":
    main()