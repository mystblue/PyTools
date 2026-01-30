import pandas as pd
from datetime import datetime
import yfinance as yf

def fetch_data(code, name):
    ticker = yf.Ticker(code + ".T")
    data = ticker.history(interval="1h", period="2d")
    data.to_csv(name + "_1h.csv")

if __name__ == '__main__':
    fetch_data("9766", "konami")
