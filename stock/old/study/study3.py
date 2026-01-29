import pandas as pd
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv")
    return data

def fetch_data2():
    data = pd.read_csv("fujikura2.csv")
    return data

def main():
    df = fetch_data()
    df2 = fetch_data2()

    print(df)
    print(df2)
    
    df_merged = pd.concat([df, df2])
    print(df_merged)

if __name__ == "__main__":
    main()