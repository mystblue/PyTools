import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    df = pd.read_csv("fujikura.csv")
    #df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").set_index("Date")
    return df

def main():
    data = fetch_data()
    print(data)
    print(type(data))
    print(len(data))
    
if __name__ == "__main__":
    main()