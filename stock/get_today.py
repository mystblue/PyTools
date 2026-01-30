import pandas as pd
from datetime import datetime
import yfinance as yf

def fetch_data(code, name):
    ticker = yf.Ticker(code + ".T")
    data = ticker.history(period="2d")
    data.to_csv("today\\" + name + "_1d.csv")

def fetch_data_local(filepath):
    data = pd.read_csv(filepath, index_col=0)
    return data

def merge(name):
    src1 = "master_10y_20260129\\" + name + "_10y.csv"
    src2 = "today\\" + name + "_1d.csv"
    df = fetch_data_local(src1)
    df2 = fetch_data_local(src2)
    #print(df.iloc[0].name)
    #print(df2.iloc[0].name)
    
    df_diff = df.loc[df.iloc[0].name:df2.iloc[0].name]
    df_diff = df_diff[:-1]
    
    df_merged = pd.concat([df_diff, df2])
    #print(df_merged)
    df_merged.to_csv("master\\" + name + ".csv")

def update_data(code, name):
    fetch_data(code, name)
    merge(name)

if __name__ == '__main__':
    update_data("5803", "fujikura")
    update_data("6857", "advantest")
    update_data("4062", "ibiden")
    update_data("6920", "lasertec")
    update_data("4180", "appier")
    update_data("3436", "sumco")
    update_data("7735", "screen")
    update_data("7741", "hoya")
    update_data("6963", "rohm")
    update_data("6525", "kokusai")
    update_data("4063", "shinetsu")
    update_data("8035", "tel")
    update_data("5801", "furukawa")
    update_data("6902", "denso")
    update_data("4519", "chugai")
    update_data("4503", "astellas")
    update_data("4507", "shionogi")
    update_data("7974", "nintendo")
    update_data("9697", "capcom")
    update_data("7832", "bandai")
    update_data("9503", "kepco")
    update_data("9501", "tepco")
    update_data("5020", "enos")
    update_data("7011", "mhi")
    update_data("7013", "ihi")
    update_data("7012", "khi")
    update_data("8001", "itochu")
    update_data("8058", "mitsubishi")
    update_data("8031", "mitsui")
    update_data("9201", "jal")
    update_data("9202", "ana")
    update_data("4661", "olc")
    update_data("9020", "jreast")
    update_data("7203", "toyota")
    update_data("7201", "nissan")
    update_data("5401", "nipponsteel")
    update_data("5411", "jfeh")
    update_data("9101", "nyk")
    update_data("9104", "mol")
    update_data("9107", "kilne")
    update_data("2801", "kikkoman")
    update_data("2802", "ajinomoto")
    update_data("2282", "nipponham")
    update_data("8136", "sanrio")
    update_data("9766", "konami")
    update_data("9684", "squareenix")
    update_data("7269", "suzuki")
    update_data("7270", "subaru")
    update_data("6146", "disco")
    update_data("6723", "renesas")
    update_data("9984", "softbankg")
    update_data("9432", "ntt")
    update_data("9433", "kddi")
    update_data("9434", "softbank")
    update_data("4751", "cyberagent")
    update_data("4755", "rakuten")
    update_data("4689", "zh")
    update_data("6702", "fujitsu")
    update_data("6701", "nec")
    update_data("6645", "omron")
