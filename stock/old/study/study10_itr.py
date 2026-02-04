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
    for index, row in df.iterrows():
        print("index:" + index)
        print(row)
        print(type(row))
    
if __name__ == "__main__":
    main()