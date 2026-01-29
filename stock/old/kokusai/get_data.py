import yfinance as yf

fujikura = yf.Ticker("6525.T")
data = fujikura.history(period="1y")
data.to_csv("kokusai.csv")

