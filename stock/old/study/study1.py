import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv", header=None)
    return data

def main():
    data = fetch_data()
    print(data)
    print(type(data))
    print(len(data))
    
if __name__ == "__main__":
    main()