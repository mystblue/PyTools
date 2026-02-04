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
    print(df.diff())
    
if __name__ == "__main__":
    main()