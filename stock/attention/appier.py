import pandas as pd
from datetime import datetime
import yfinance as yf

def fetch_data(code, name):
    ticker = yf.Ticker(code + ".T")
    data = ticker.history(period="1d")
    data.to_csv("..\\today\\" + name + "_1d.csv")

def fetch_data_local(filepath):
    data = pd.read_csv(filepath, index_col=0)
    return data

def merge(name):
    src1 = "..\\master_10y_20260129\\" + name + "_10y.csv"
    src2 = "..\\today\\" + name + "_1d.csv"
    df = fetch_data_local(src1)
    df2 = fetch_data_local(src2)
    #print(df.iloc[0].name)
    #print(df2.iloc[0].name)
    
    df_diff = df.loc[df.iloc[0].name:df2.iloc[0].name]
    df_diff = df_diff[:-1]
    
    df_merged = pd.concat([df_diff, df2])
    #print(df_merged)
    df_merged.to_csv("..\\master\\" + name + ".csv")

def update_data(code, name):
    fetch_data(code, name)
    #merge(name)

if __name__ == '__main__':
    update_data("4180", "appier")
