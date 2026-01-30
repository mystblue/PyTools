import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

# ===== パラメータ =====
#TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "appier", "sumco", "screen", "hoya", "rohm", "kokusai", "shinetsu", "tel"]
TICKERS = ["konami"]
START = "2016-01-28"
END = None  # None なら最新まで

def fetch_data(ticker):
    data = pd.read_csv(ticker + "_10y.csv")

    return data

# ===== テクニカル付与 =====
def add_indicators(df):
    df["MA5"] = df["Close"].rolling(window=5).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()
    
    # 25 日線が上向きを追加
    df["MA25"] = df["Close"].rolling(25).mean()
    df["MA25_SLOPE"] = df["MA25"].diff()

    # 75 日線が上向きを追加
    df["MA75"] = df["Close"].rolling(75).mean()
    df["MA75_SLOPE"] = df["MA75"].diff()

    return df

# ===== 改善後ルール：買いシグナル判定（その日の終値ベース） =====
def is_buy_signal(latest, prev):
    #latest = df.iloc[-1]
    #prev = df.iloc[-2]

    # ゴールデンクロス（MA5がMA20を上抜け）
    gc = (prev["MA5"] <= prev["MA20"]) and (latest["MA5"] > latest["MA20"])

    # 出来高が平均以上
    vol_ok = latest["Volume"] > latest["VOLUME_MA20"]

    # RSIが50以上（弱すぎない）
    #rsi_ok = latest["RSI14"] >= 50
    rsi_ok = latest["RSI14"] >= 45

    # MACDがシグナル上抜け
    #macd_ok = (prev["MACD"] <= prev["MACD_SIGNAL"]) and (latest["MACD"] > latest["MACD_SIGNAL"])

    cond6 = latest["MA25_SLOPE"] > 0

    cond75 = latest["MA75_SLOPE"] > 0

    #return gc and vol_ok and rsi_ok and macd_ok
    #return vol_ok and rsi_ok and macd_ok
    return gc and vol_ok and rsi_ok and cond6 and cond75

# ===== 売りシグナル（20MA割れ） =====
def is_sell_signal(daily_row_prev, daily_row):
    return (daily_row_prev["Close"] >= daily_row_prev["MA20"]) and (daily_row["Close"] < daily_row["MA20"])

def max_drawdown(equity):
    s = pd.Series(equity)
    peak = s.cummax()
    dd = (s - peak) / peak
    return dd.min()

# ===== 1銘柄バックテスト =====
def backtest_single(ticker):
    print(f"=== Backtest: {ticker} ===")
    equity = [1.0]   # 初期資産を1.0とする

    data = fetch_data(ticker)

    if len(data) < 200:
        print("データ不足")
        return None

    data = add_indicators(data)

    # 欠損除去
    data = data.dropna()

    position = 0  # 0: ノーポジ, 1: ロング
    entry_price = 0.0
    trades = []

    # 日足を1本ずつ進める（翌日の始値で約定する前提）
    for i in range(21, len(data) - 1):
        today = data.iloc[i]
        #print(today)
        yesterday = data.iloc[i - 1]
        tomorrow = data.iloc[i + 1]  # 約定価格用

        # 売り判定（ポジションありのとき）
        if position == 1 and is_sell_signal(yesterday, today):
            exit_price = tomorrow["Open"]
            pl = exit_price - entry_price
            equity.append(equity[-1] * (1 + pl / entry_price))
            print("■売り")
            print(today["Date"])
            print("利益 = " + str(exit_price) + " - " + str(entry_price))
            print(pl)
            trades.append(pl)
            position = 0
            entry_price = 0.0

        # 買い判定（ノーポジのとき）
        if position == 0 and is_buy_signal(today, yesterday):
            print("■買い")
            print(today["Date"])
            entry_price = tomorrow["Open"]
            position = 1

    # 最後までポジションが残っていたら、最終日の終値でクローズ
    if position == 1:
        last_close = data.iloc[-1]["Close"]
        pl = last_close - entry_price
        equity.append(equity[-1] * (1 + pl / entry_price))
        print("■売り")
        print(today["Date"])
        print("利益 = " + str(last_close) + " - " + str(entry_price))
        print(pl)
        trades.append(pl)

    if len(trades) == 0:
        print("トレードなし")
        return {
            "ticker": ticker,
            "trades": 0,
            "win_rate": None,
            "total_pl": 0.0,
            "avg_pl": None,
        }

    wins = [t for t in trades if t > 0]
    win_rate = len(wins) / len(trades)
    total_pl = sum(trades)
    avg_pl = total_pl / len(trades)

    wins2 = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]

    total_profit = sum(wins2)
    total_loss = abs(sum(losses)) if losses else 0.0

    # 
    pf = total_profit / total_loss if total_loss > 0 else float("inf")
    
    # 最大ドローダウン
    dd = max_drawdown(equity)


    result = {
        "ticker": ticker,
        "trades": len(trades),
        "win_rate": win_rate,
        "total_pl": total_pl,
        "avg_pl": avg_pl,
        "pf": pf,
        "dd": dd,
    }
    print(result)
    return result

# ===== 複数銘柄まとめてバックテスト =====
def main():
    results = []
    for ticker in TICKERS:
        res = backtest_single(ticker)
        if res is not None:
            results.append(res)

    if not results:
        print("結果なし")
        return

    df = pd.DataFrame(results)
    print("\n=== Summary ===")
    print(df)

    print("\n平均勝率:", df["win_rate"].mean())
    print("合計損益:", df["total_pl"].sum())
    print("平均損益/トレード:", df["avg_pl"].mean())
    print("プロフィットファクター:", df["pf"].mean())
    print("平均DD:", df["dd"].mean())

if __name__ == "__main__":
    main()