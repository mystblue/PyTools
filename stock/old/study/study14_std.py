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
    print(df)
    print(df["Close"].std())
    print(df["Close"].rolling(5).std())
    
if __name__ == "__main__":
    main()