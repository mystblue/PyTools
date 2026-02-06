import pandas as pd
import mplfinance as mpf

def create_chart(df):
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA25"] = df["Close"].rolling(25).mean()
    df["MA75"] = df["Close"].rolling(75).mean()
    
    # --- RSI 計算（14日） ---
    window = 14
    delta = df["Close"].diff()
    
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.ewm(alpha=1/window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    df = df.tail(30)  # 直近60営業日
    
    apds = [
        mpf.make_addplot(df["MA5"], panel=0, width=1, color="magenta"),
        mpf.make_addplot(df["MA25"], panel=0, width=1, color="green"),
        mpf.make_addplot(df["MA75"], panel=0, width=1, color="orange"),
        mpf.make_addplot(df["RSI"], panel=2, width=1, color="blue")
    ]
    
    mc = mpf.make_marketcolors(
        up='red',
        down='blue',
        wick={'up':'red', 'down':'blue'},
        volume={'up':'red','down':'blue'}
    )
    
    mystyle = mpf.make_mpf_style(
        base_mpf_style='yahoo',
        marketcolors=mc
    )
    
    # ローソク足チャート表示
    mpf.plot(
        df,
        type="candle",
        volume=True,
        #mav=(5, 25, 75),
        style="yahoo",
        datetime_format="%m-%d",   # ← 日付フォーマット指定
        xrotation=0,               # ← これで横向きになる
        #show_nontrading=True,   # ← 土日も含めて日付が連続
        addplot=apds,
        panel_ratios=(4,1,1),
        savefig="candlestick.png"
    )

def create_chart_bb(df):
	# --- ボリンジャーバンド計算（20日・2σ） ---
	window = 20
	df["MA20"] = df["Close"].rolling(window).mean()
	df["STD20"] = df["Close"].rolling(window).std()
	
	df["Upper"] = df["MA20"] + (df["STD20"] * 2)
	df["Lower"] = df["MA20"] - (df["STD20"] * 2)
    
	df["MA160"] = df["Close"].rolling(160).mean()
	
	#df_period = df["2024-01-01":"2024-03-31"]
	df = df.tail(30)  # 直近60営業日
	#df = df["2025-01-17":"2025-02-01"]
	
	apds = [
	    mpf.make_addplot(df["MA20"], panel=0, width=1, color="blue", label="middle"),
	    mpf.make_addplot(df["Upper"], panel=0, width=1, color="green", label="2σ"),
	    mpf.make_addplot(df["Lower"], panel=0, width=1, color="red", label="-2σ"),
	    mpf.make_addplot(df["MA160"], panel=0, width=1, color="brown", label="160"),
	]

	mc = mpf.make_marketcolors(
	    up='red',
	    down='blue',
	    wick={'up':'red', 'down':'blue'},
	    volume={'up':'red','down':'blue'}
	)

	mystyle = mpf.make_mpf_style(
	    base_mpf_style='yahoo',
	    marketcolors=mc
	)

	# ローソク足チャート表示
	mpf.plot(
	    df,
	    type="candle",
	    volume=False,
	    #mav=(5, 25, 75),
	    style="yahoo",
	    datetime_format="%m-%d",   # ← 日付フォーマット指定
	    xrotation=0,               # ← これで横向きになる
	    #show_nontrading=True,   # ← 土日も含めて日付が連続
	    addplot=apds,
	    savefig="candlestick2.png"
	)

if __name__ == '__main__':
    # CSV 読み込み
    df = pd.read_csv("..\\master\\simizu.csv", parse_dates=["Date"], index_col="Date")
    create_chart(df)
    create_chart_bb(df)
