import pandas as pd
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv", index_col=0)
    return data

def main():
    df = fetch_data()
    print(df.iloc[0])
    print(type(df.iloc[0]))
    print(df.iloc[1])

    print("複数選択")
    print(df.iloc[0:2])

    print("複数選択")
    print(df.loc["2026-01-16 00:00:00+09:00":"2026-01-26 00:00:00+09:00"])

if __name__ == "__main__":
    main()