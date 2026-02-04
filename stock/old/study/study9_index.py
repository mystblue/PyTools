import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    df = pd.read_csv("fujikura.csv")
    df = df.sort_values("Date").set_index("Date")
    return df

def main():
    data = fetch_data()
    print(data.index)
    print(data.index[0])
    print(data.index[0:2])
    print(data.at["2026-01-15 00:00:00+09:00", "Close"])
    
if __name__ == "__main__":
    main()