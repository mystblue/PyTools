import pandas as pd
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv", index_col=0)
    return data

def main():
    df = fetch_data()
    print(df)
    #print(df.at["2026-01-21"])
    print(df.at['2026-01-21 00:00:00+09:00', 'Close'])

if __name__ == "__main__":
    main()