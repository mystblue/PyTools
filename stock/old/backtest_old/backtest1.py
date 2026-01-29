import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

# ===== パラメータ =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]
START = "2015-01-01"
END = None  # None なら最新まで

# ===== データ取得 =====
def fetch_daily(ticker, start=START, end=END):
    df = yf.download(ticker, start=start, end=end, interval="1d", progress=False)
    df.dropna(inplace=True)
    return df

def fetch_weekly(ticker, start=START, end=END):
    df = yf.download(ticker, start=start, end=end, interval="1wk", progress=False)
    df.dropna(inplace=True)
    return df

# ===== テクニカル付与 =====
def add_daily_indicators(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["VOL_MA20"] = df["Volume"].rolling(20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], 14).rsi()
    return df

def add_weekly_indicators(df):
    df["W_MA20"] = df["Close"].rolling(20).mean()
    return df

# ===== 改善後ルール：買いシグナル判定（その日の終値ベース） =====
def is_buy_signal(daily_row_prev, daily_row, weekly_row):
    # 1. 20MAブレイク
    cond_break = (daily_row_prev["Close"] <= daily_row_prev["MA20"]) and (daily_row["Close"] > daily_row["MA20"])
    # 2. 20MA上向き
    cond_ma_up = daily_row["MA20"] > daily_row_prev["MA20"]
    # 3. RSI >= 50
    cond_rsi = daily_row["RSI14"] >= 50
    # 4. 出来高 >= 20日平均
    cond_vol = daily_row["Volume"] >= daily_row["VOL_MA20"]
    # 5. 週足20MAの上
    cond_week = weekly_row["Close"] > weekly_row["W_MA20"]

    return all([cond_break, cond_ma_up, cond_rsi, cond_vol, cond_week])

# ===== 売りシグナル（20MA割れ） =====
def is_sell_signal(daily_row_prev, daily_row):
    return (daily_row_prev["Close"] >= daily_row_prev["MA20"]) and (daily_row["Close"] < daily_row["MA20"])

# ===== 1銘柄バックテスト =====
def backtest_single(ticker):
    print(f"=== Backtest: {ticker} ===")
    daily = fetch_daily(ticker)
    weekly = fetch_weekly(ticker)

    if len(daily) < 200 or len(weekly) < 30:
        print("データ不足")
        return None

    daily = add_daily_indicators(daily)
    weekly = add_weekly_indicators(weekly)

    # 欠損除去
    daily = daily.dropna()
    weekly = weekly.dropna()

    # 週足を日足に合わせて forward fill
    weekly_ff = weekly[["Close", "W_MA20"]].rename(columns={"Close": "W_Close"})
    weekly_ff = weekly_ff.reindex(daily.index, method="ffill")
    merged = daily.join(weekly_ff, how="inner")

    position = 0  # 0: ノーポジ, 1: ロング
    entry_price = 0.0
    trades = []

    # 日足を1本ずつ進める（翌日の始値で約定する前提）
    for i in range(21, len(merged) - 1):
        today = merged.iloc[i]
        yesterday = merged.iloc[i - 1]
        tomorrow = merged.iloc[i + 1]  # 約定価格用

        # 売り判定（ポジションありのとき）
        if position == 1 and is_sell_signal(yesterday, today):
            exit_price = tomorrow["Open"]
            pl = exit_price - entry_price
            trades.append(pl)
            position = 0
            entry_price = 0.0

        # 買い判定（ノーポジのとき）
        if position == 0 and is_buy_signal(yesterday, today, today[["W_Close", "W_MA20"]].rename({"W_Close": "Close"})):
            entry_price = tomorrow["Open"]
            position = 1

    # 最後までポジションが残っていたら、最終日の終値でクローズ
    if position == 1:
        last_close = merged.iloc[-1]["Close"]
        pl = last_close - entry_price
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

    result = {
        "ticker": ticker,
        "trades": len(trades),
        "win_rate": win_rate,
        "total_pl": total_pl,
        "avg_pl": avg_pl,
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

if __name__ == "__main__":
    main()