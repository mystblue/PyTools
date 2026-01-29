import yfinance as yf

fujikura = yf.Ticker("4062.T")
data = fujikura.history(period="1y")
data.to_csv("ibiden.csv")

