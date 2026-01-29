import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ===== パラメータ =====
TICKERS = ["NVDA", "AMD", "AVGO", "TSM", "MSFT", "GOOGL"]
START = "2015-01-01"
END = None

# ===== RSI 自作 =====
def calc_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)

    ma_up = up.rolling(period).mean()
    ma_down = down.rolling(period).mean()

    rsi = 100 - (100 / (1 + (ma_up / ma_down)))
    return rsi

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
    df["RSI14"] = calc_rsi(df["Close"], 14)
    return df.dropna()

def add_weekly_indicators(df):
    df["W_MA20"] = df["Close"].rolling(20).mean()
    return df.dropna()

# ===== 週足 → 日足に変換 =====
def convert_weekly_to_daily(weekly_df, daily_index):
    return weekly_df.reindex(daily_index, method="ffill")

# ===== 最大ドローダウン =====
def max_drawdown(equity_list):
    s = pd.Series(equity_list)
    peak = s.cummax()
    dd = (s - peak) / peak
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

    # 週足を日足に変換
    weekly_small = weekly[["Close", "W_MA20"]].rename(columns={"Close": "W_Close"})
    weekly_daily = convert_weekly_to_daily(weekly_small, daily.index)

    # 完全に1行対応の df を作る
    df = pd.concat([daily, weekly_daily], axis=1).dropna()

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
            sell_cond = (prev["Close"] >= prev["MA20"]) and (today["Close"] < today["MA20"])
            if sell_cond:
                exit_price = tomorrow["Open"]
                pl = exit_price - entry_price
                trades.append(pl)
                equity.append(equity[-1] * (1 + pl / entry_price))
                position = 0
                entry_price = 0.0
                continue

        # 買い条件（ノーポジのみ）
        if position == 0:
            cond1 = (prev["Close"] <= prev["MA20"]) and (today["Close"] > today["MA20"])
            cond2 = today["MA20"] > prev["MA20"]
            cond3 = today["RSI14"] >= 50
            cond4 = today["Volume"] >= today["VOL_MA20"]
            cond5 = today["W_Close"] > today["W_MA20"]

            if all([cond1, cond2, cond3, cond4, cond5]):
                entry_price = tomorrow["Open"]
                position = 1

        equity.append(equity[-1])

    # 最後にポジションが残っていたらクローズ
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
    dd = max_drawdown(equity)

    result = {
        "ticker": ticker,
        "trades": len(trades),
        "win_rate": win_rate,
        "avg_pl": avg_pl,
        "pf": pf,
        "dd": dd,
        "equity": equity,
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
        plt.plot(r["equity"], label=r["ticker"])
    plt.title("Equity Curve (Kenji Trend Rule)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()