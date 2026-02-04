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
    print(df.iloc[0])
    print(type(df.iloc[0]))
    series = df.iloc[0]
    print(series["Close"])
    print(series.name)
    print(series > 1000)
    print(series[0:2])
    
if __name__ == "__main__":
    main()