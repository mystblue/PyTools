import yfinance as yf

fujikura = yf.Ticker("1803.T")
data = fujikura.history(period="10y")
data.to_csv("simizu_10y.csv")

#print(data)
#print(type(data))
#with open("fujikura.csv", "w", encoding="utf-8") as f:
#    f.write(str(data))