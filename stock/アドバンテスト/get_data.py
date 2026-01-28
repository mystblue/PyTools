import yfinance as yf

fujikura = yf.Ticker("6857.T")
data = fujikura.history(period="1y")
data.to_csv("advantest.csv")

