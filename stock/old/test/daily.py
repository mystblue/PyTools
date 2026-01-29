import yfinance as yf

fujikura = yf.Ticker("5803.T")
data = fujikura.history(period="1d")
data.to_csv("fujikura_1d.csv")

print(data)
print(type(data))
#with open("fujikura.csv", "w", encoding="utf-8") as f:
#    f.write(str(data))