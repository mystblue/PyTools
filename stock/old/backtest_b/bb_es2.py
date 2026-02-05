import pandas as pd
import numpy as np

# =========================
# 設定
# =========================
#CSV_PATH = "price_data.csv"
CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス
BB_PERIOD = 20
BB_STD = 2
BBW_LOOKBACK = 20

# =========================
# インジケーター計算
# =========================
def compute_indicators(df):
    df["MB"] = df["Close"].rolling(BB_PERIOD).mean()
    df["STD"] = df["Close"].rolling(BB_PERIOD).std()
    df["UB"] = df["MB"] + BB_STD * df["STD"]
    df["LB"] = df["MB"] - BB_STD * df["STD"]

    df["BBW"] = (df["UB"] - df["LB"]) / df["MB"]
    df["BBW_MA"] = df["BBW"].rolling(BBW_LOOKBACK).mean()

    return df

# =========================
# データ読み込み
# =========================
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip().capitalize() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

df = compute_indicators(df)

# =========================
# バックテスト本体
# =========================
trades = []
position = None

for i in range(1, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]

    # インジケーター不足ならスキップ
    if pd.isna(row["BBW_MA"]) or pd.isna(row["UB"]) or pd.isna(row["MB"]):
        continue

    # =========================
    # エグジット：ミドルバンド割れ
    # =========================
    if position is not None:
        entry_price = position["entry_price"]

        if close < row["MB"]:
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
            continue

    # =========================
    # エントリー条件
    # =========================
    if position is None:

        # 収縮（BBWが平均以下）
        cond_squeeze = row["BBW"] < row["BBW_MA"]

        # 拡大（ヒゲでも上バンド突破）
        cond_breakout = (prev["High"] <= prev["UB"]) and (row["High"] > row["UB"])

        if cond_squeeze and cond_breakout:
            position = {
                "entry_date": date,
                "entry_price": close,
            }

# =========================
# 結果集計
# =========================
trades_df = pd.DataFrame(trades)

if len(trades_df) == 0:
    print("トレードが発生しませんでした。パラメータや銘柄を確認してください。")
else:
    win_trades = trades_df[trades_df["return"] > 0]
    lose_trades = trades_df[trades_df["return"] <= 0]

    total_trades = len(trades_df)
    win_rate = len(win_trades) / total_trades * 100
    avg_ret = trades_df["return"].mean() * 100
    avg_win = win_trades["return"].mean() * 100 if len(win_trades) else 0
    avg_loss = lose_trades["return"].mean() * 100 if len(lose_trades) else 0
    cum_ret = (1 + trades_df["return"]).prod() - 1

    equity_curve = (1 + trades_df["return"]).cumprod()
    peak = equity_curve.cummax()
    dd_series = (equity_curve / peak - 1) * 100
    max_dd = dd_series.min()

    print("===== BBW < BBW_MA20 × High > UB × MB割れ =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"累積リターン      : {cum_ret*100:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())