import pandas as pd
from datetime import datetime

def fetch_data():
    data = pd.read_csv("fujikura.csv", index_col=0)
    return data

def fetch_data2():
    data = pd.read_csv("fujikura3.csv", index_col=0)
    return data

def main():
    df = fetch_data()
    df2 = fetch_data2()
    print(df)
    print(df2)
    print("■")
    print(df2.iloc[0])
    print(type(df2.iloc[0]))
    print(df.iloc[0]["Open"])
    print(df.iloc[0]["Close"])
    print(df.iloc[0].name)
    print(df2.iloc[0].name)
    
    df_diff = df.loc[df.iloc[0].name:df2.iloc[0].name]
    df_diff = df_diff[:-1]
    
    df_merged = pd.concat([df_diff, df2])
    print(df_merged)

if __name__ == "__main__":
    main()