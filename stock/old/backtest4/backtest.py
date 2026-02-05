import pandas as pd
import numpy as np

# ===== 設定 =====
CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス
RISK_CUT = -0.05             # 損切り -5%
TAKE_PROFIT = 0.10           # 利確 +20%
RSI_PERIOD = 14

# ===== RSI計算関数 =====
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)

    gain_rolling = pd.Series(gain).rolling(window=period, min_periods=period).mean()
    loss_rolling = pd.Series(loss).rolling(window=period, min_periods=period).mean()

    rs = gain_rolling / loss_rolling
    rsi = 100 - (100 / (1 + rs))
    rsi.index = series.index
    return rsi

# ===== データ読み込み =====
df = pd.read_csv(CSV_PATH)

# 列名の標準化（必要に応じて調整）
df.columns = [c.strip().capitalize() for c in df.columns]
# 期待する列: Date, Open, High, Low, Close, Volume

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# ===== インジケーター計算 =====
df["MA5"] = df["Close"].rolling(window=5).mean()
df["MA25"] = df["Close"].rolling(window=25).mean()
df["RSI14"] = compute_rsi(df["Close"], period=RSI_PERIOD)
df["Vol_prev"] = df["Volume"].shift(1)
df["Vol_ratio"] = df["Volume"] / df["Vol_prev"]

# ゴールデンクロス状態（5MA > 25MA）
df["GC_state"] = df["MA5"] > df["MA25"]

# ===== バックテスト =====
trades = []  # 各トレードの記録
position = None  # {"entry_date", "entry_price", "size"} など
equity = 1_000_000  # 仮の初期資金（使わなくてもOK、将来拡張用）

for i in range(1, len(df)):
    row = df.iloc[i]
    prev_row = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]
    high = row["High"]
    low = row["Low"]

    # すでにポジションを持っている場合：利確 or 損切り判定
    if position is not None:
        entry_price = position["entry_price"]

        tp_price = entry_price * (1 + TAKE_PROFIT)
        sl_price = entry_price * (1 + RISK_CUT)

        exit_reason = None
        exit_price = None

        # 高値が利確ラインを超えた場合
        if high >= tp_price:
            exit_price = tp_price
            exit_reason = "TP"

        # 安値が損切りラインを割った場合
        elif low <= sl_price:
            exit_price = sl_price
            exit_reason = "SL"

        # エグジットが発生したらトレード確定
        if exit_reason is not None:
            ret = (exit_price - entry_price) / entry_price

            trades.append({
                "entry_date": position["entry_date"],
                "entry_price": entry_price,
                "exit_date": date,
                "exit_price": exit_price,
                "return": ret,
                "reason": exit_reason,
            })

            position = None  # ノーポジに戻る

    # ポジションを持っていない場合：新規エントリー判定
    if position is None:
        # 必要な値がNaNならスキップ
        if pd.isna(row["MA5"]) or pd.isna(row["MA25"]) or pd.isna(row["RSI14"]) or pd.isna(row["Vol_ratio"]):
            continue

        # エントリー条件：
        # 1. GC状態（5MA > 25MA）
        # 2. 終値 < 5MA（押し目）
        # 3. RSI14 <= 40
        # 4. 出来高 >= 前日比120%
        cond_gc = row["GC_state"]
        cond_pullback = close < row["MA5"]
        cond_rsi = row["RSI14"] <= 40
        cond_vol = row["Vol_ratio"] >= 1.1

        if cond_gc and cond_pullback and cond_rsi and cond_vol:
            position = {
                "entry_date": date,
                "entry_price": close,
            }

# ===== 結果集計 =====
trades_df = pd.DataFrame(trades)

if len(trades_df) == 0:
    print("トレードが一度も発生しませんでした。条件が厳しすぎる可能性があります。")
else:
    win_trades = trades_df[trades_df["return"] > 0]
    lose_trades = trades_df[trades_df["return"] <= 0]

    total_trades = len(trades_df)
    win_rate = len(win_trades) / total_trades * 100
    avg_ret = trades_df["return"].mean() * 100
    avg_win = win_trades["return"].mean() * 100 if len(win_trades) > 0 else 0.0
    avg_loss = lose_trades["return"].mean() * 100 if len(lose_trades) > 0 else 0.0
    max_dd = trades_df["return"].cumsum().min() * 100  # 累積リターンベースの簡易DD

    print("===== バックテスト結果 =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%（累積リターンベース簡易）")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())