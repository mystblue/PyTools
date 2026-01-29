import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

# ===== パラメータ =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]
START = "2015-01-01"
END = None

# ===== データ取得 =====
def fetch_daily(ticker):
    df = yf.download(ticker, start=START, end=END, interval="1d", progress=False)
    df.dropna(inplace=True)
    return df

def fetch_weekly(ticker):
    df = yf.download(ticker, start=START, end=END, interval="1wk", progress=False)
    df.dropna(inplace=True)
    return df

# ===== テクニカル =====
def add_daily_indicators(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["VOL_MA20"] = df["Volume"].rolling(20).mean()
    df["RSI14"] = ta.momentum.RSIIndicator(df["Close"], 14).rsi()
    return df.dropna()

def add_weekly_indicators(df):
    df["W_MA20"] = df["Close"].rolling(20).mean()
    return df.dropna()

# ===== 最大ドローダウン =====
def max_drawdown(equity_series: pd.Series):
    peak = equity_series.cummax()
    dd = (equity_series - peak) / peak
    return dd.min()

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

    # 週足を日足に合わせて前方埋め
    weekly_ff = weekly[["Close", "W_MA20"]].rename(columns={"Close": "W_Close"})
    weekly_ff = weekly_ff.reindex(daily.index, method="ffill")

    df = daily.join(weekly_ff, how="inner").dropna()

    position = 0
    entry_price = 0.0
    trades = []
    equity = [1.0]  # 資産1.0スタート

    for i in range(1, len(df) - 1):
        prev = df.iloc[i - 1]
        today = df.iloc[i]
        tomorrow = df.iloc[i + 1]

        # 売り条件：20MA割れ
        if position == 1:
            if (prev["Close"] >= prev["MA20"]) and (today["Close"] < today["MA20"]):
                exit_price = tomorrow["Open"]
                pl = exit_price - entry_price
                trades.append(pl)
                equity.append(equity[-1] * (1 + pl / entry_price))
                position = 0
                entry_price = 0.0
            else:
                equity.append(equity[-1])
                continue

        # 買い条件（ノーポジ時のみ）
        if position == 0:
            cond1 = (prev["Close"] <= prev["MA20"]) and (today["Close"] > today["MA20"])
            cond2 = today["MA20"] > prev["MA20"]
            cond3 = today["RSI14"] >= 50
            cond4 = today["Volume"] >= today["VOL_MA20"]
            cond5 = (today["W_Close"] > today["W_MA20"])

            if all([cond1, cond2, cond3, cond4, cond5]):
                entry_price = tomorrow["Open"]
                position = 1

            equity.append(equity[-1])

    # 最後までポジションが残っていたらクローズ
    if position == 1:
        last_close = df.iloc[-1]["Close"]
        pl = last_close - entry_price
        trades.append(pl)
        equity.append(equity[-1] * (1 + pl / entry_price))

    if len(trades) == 0:
        print("トレードなし")
        return None

    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]

    total_profit = sum(wins)
    total_loss = abs(sum(losses)) if losses else 0.0
    pf = (total_profit / total_loss) if total_loss > 0 else float("inf")
    avg_pl = sum(trades) / len(trades)
    win_rate = len(wins) / len(trades)

    equity_series = pd.Series(equity)
    dd = max_drawdown(equity_series)

    result = {
        "ticker": ticker,
        "trades": len(trades),
        "win_rate": win_rate,
        "avg_pl": avg_pl,
        "pf": pf,
        "dd": dd,
        "equity": equity_series,
    }
    print(result)
    return result

# ===== 全銘柄バックテスト =====
def main():
    results = []
    for t in TICKERS:
        res = backtest_single(t)
        if res:
            results.append(res)

    if not results:
        print("結果なし")
        return

    df = pd.DataFrame([{
        "ticker": r["ticker"],
        "trades": r["trades"],
        "win_rate": r["win_rate"],
        "avg_pl": r["avg_pl"],
        "pf": r["pf"],
        "dd": r["dd"],
    } for r in results])

    print("\n=== Summary ===")
    print(df)
    print("\n平均PF:", df["pf"].mean())
    print("平均DD:", df["dd"].mean())

    # 損益曲線プロット
    plt.figure(figsize=(12, 6))
    for r in results:
        plt.plot(r["equity"].values, label=r["ticker"])
    plt.title("Equity Curve (Kenji Trend Rule)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()