import pandas as pd
import numpy as np

# ===== 設定 =====
CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス

# ===== ATR計算 =====
def compute_atr(df, period=14):
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift(1)).abs()
    low_close = (df["Low"] - df["Close"].shift(1)).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

# ===== ボリンジャーバンド計算 =====
def compute_bbands(df, window=20, num_std=2):
    df["MB"] = df["Close"].rolling(window).mean()
    df["STD"] = df["Close"].rolling(window).std()
    df["UB"] = df["MB"] + num_std * df["STD"]
    df["LB"] = df["MB"] - num_std * df["STD"]
    return df

# ===== データ読み込み =====
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip().capitalize() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# ===== インジケーター計算 =====
df["SMA200"] = df["Close"].rolling(window=300).mean()
df = compute_bbands(df)

df["ATR"] = compute_atr(df, period=14)
df["ATR_MA20"] = df["ATR"].rolling(20).mean()

df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()
df["SMA50"] = df["Close"].rolling(50).mean()


# ===== バックテスト =====
trades = []
position = None

for i in range(1, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]

    # 必要な値がNaNならスキップ
    if pd.isna(row["UB"]) or pd.isna(row["MB"]) or pd.isna(row["SMA200"]):
        continue

    # ===== エグジット =====
    if position is not None:
        entry_price = position["entry_price"]

        # エグジット：SMA50割れ
        if close < row["SMA50"]:
            ret = (close - entry_price) / entry_price

            trades.append({
                "entry_date": position["entry_date"],
                "entry_price": entry_price,
                "exit_date": date,
                "exit_price": close,
                "return": ret,
                "reason": "MB_break",
            })

            position = None

    # ===== エントリー =====
    if position is None:
        #cond_breakout = (prev["Close"] <= prev["UB"] * 1.01) and (close > row["UB"] * 1.01)
        cond_breakout = close > row["UB"] * 0.9
        cond_trend = close > row["SMA200"]
        vol_ok = row["Volume"] > row["VOLUME_MA20"]
        cond_atr = row["ATR"] > row["ATR_MA20"]

        if cond_breakout and cond_trend:
            position = {
                "entry_date": date,
                "entry_price": close,
            }

# ===== 結果集計 =====
trades_df = pd.DataFrame(trades)

if len(trades_df) == 0:
    print("トレードが発生しませんでした。条件が厳しすぎる可能性があります。")
else:
    win_trades = trades_df[trades_df["return"] > 0]
    lose_trades = trades_df[trades_df["return"] <= 0]

    total_trades = len(trades_df)
    win_rate = len(win_trades) / total_trades * 100
    avg_ret = trades_df["return"].mean() * 100
    avg_win = win_trades["return"].mean() * 100 if len(win_trades) > 0 else 0
    avg_loss = lose_trades["return"].mean() * 100 if len(lose_trades) > 0 else 0
    max_dd = trades_df["return"].cumsum().min() * 100

    print("===== ボリンジャーバンド順張りバックテスト結果 =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%（累積ベース簡易）")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())
    print("\n--- トレード一覧（末尾5件） ---")
    print(trades_df.tail(10))
    