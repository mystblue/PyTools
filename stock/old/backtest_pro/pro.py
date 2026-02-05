import pandas as pd
import numpy as np

# =========================
# 設定
# =========================
#CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス
CSV_PATH = "..\\..\\master\\appier.csv"  # 日足データのCSVパス
DONCHIAN_ENTRY = 20           # エントリー用ドンチャン期間（高値）
DONCHIAN_EXIT = 10            # エグジット用ドンチャン期間（安値）
SMA_LONG = 300                # 長期トレンド判定用SMA

# =========================
# インジケーター計算
# =========================
def compute_indicators(df):
    df["SMA_LONG"] = df["Close"].rolling(SMA_LONG).mean()
    df["DC_HIGH"] = df["High"].rolling(DONCHIAN_ENTRY).max()
    df["DC_LOW"] = df["Low"].rolling(DONCHIAN_EXIT).min()
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
position = None  # {"entry_date":..., "entry_price":...}

for i in range(1, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]

    # 必要な指標がNaNならスキップ
    if pd.isna(row["SMA_LONG"]) or pd.isna(row["DC_HIGH"]) or pd.isna(row["DC_LOW"]):
        continue

    # =========================
    # エグジット（Donchian 10日安値割れ）
    # =========================
    if position is not None:
        entry_price = position["entry_price"]

        # 終値がドンチャン下限（10日安値）を下抜けたら手仕舞い
        if close < row["DC_LOW"]:
            ret = (close - entry_price) / entry_price

            trades.append({
                "entry_date": position["entry_date"],
                "entry_price": entry_price,
                "exit_date": date,
                "exit_price": close,
                "return": ret,
                "reason": "DC10_break",
            })

            position = None

    # =========================
    # エントリー（SMA300上＆Donchian20高値ブレイク）
    # =========================
    if position is None:
        # 長期上昇トレンド
        cond_trend = close > row["SMA_LONG"]

        # Donchian 20 高値ブレイク（前日までは抜けていない）
        cond_breakout = (prev["Close"] <= prev["DC_HIGH"]) and (close > row["DC_HIGH"])

        if cond_trend and cond_breakout:
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
    avg_win = win_trades["return"].mean() * 100 if len(win_trades) > 0 else 0
    avg_loss = lose_trades["return"].mean() * 100 if len(lose_trades) > 0 else 0
    cum_ret = (1 + trades_df["return"]).prod() - 1

    # 簡易DD（累積リターンベース）
    equity_curve = (1 + trades_df["return"]).cumprod()
    peak = equity_curve.cummax()
    dd_series = (equity_curve / peak - 1) * 100
    max_dd = dd_series.min()

    print("===== プロ仕様 Donchian × SMA300 順張りバックテスト結果 =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"累積リターン      : {cum_ret*100:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%（累積リターンベース簡易）")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())
    print("\n--- トレード一覧（末尾10件） ---")
    print(trades_df.tail(10))