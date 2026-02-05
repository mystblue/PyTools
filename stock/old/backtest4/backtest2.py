import pandas as pd
import numpy as np

# ===== 設定 =====
#CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス
CSV_PATH = "..\\..\\master\\konami.csv"  # 日足データのCSVパス
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
df.columns = [c.strip().capitalize() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# ===== インジケーター計算 =====
df["MA5"] = df["Close"].rolling(window=5).mean()
df["MA25"] = df["Close"].rolling(window=25).mean()
df["RSI14"] = compute_rsi(df["Close"], period=RSI_PERIOD)
df["Vol_prev"] = df["Volume"].shift(1)
df["Vol_ratio"] = df["Volume"] / df["Vol_prev"]

# ゴールデンクロス発生日を特定
df["GC_signal"] = (df["MA5"] > df["MA25"]) & (df["MA5"].shift(1) <= df["MA25"].shift(1))

# GC後フラグ（GC発生後は True を維持）
df["GC_after"] = False
gc_flag = False
for i in range(len(df)):
    if df.loc[i, "GC_signal"]:
        gc_flag = True
    df.loc[i, "GC_after"] = gc_flag

# 5MAが上向き（上昇継続）
df["MA5_up"] = df["MA5"] > df["MA5"].shift(1)

# ===== バックテスト =====
trades = []
position = None

for i in range(1, len(df)):
    row = df.iloc[i]
    prev_row = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]
    high = row["High"]
    low = row["Low"]

    # ポジション保有中：利確 or 損切り
    if position is not None:
        entry_price = position["entry_price"]

        tp_price = entry_price * (1 + TAKE_PROFIT)
        sl_price = entry_price * (1 + RISK_CUT)

        exit_reason = None
        exit_price = None

        if high >= tp_price:
            exit_price = tp_price
            exit_reason = "TP"
        elif low <= sl_price:
            exit_price = sl_price
            exit_reason = "SL"

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

            position = None

    # ノーポジ：新規エントリー判定
    if position is None:

        # 必要な値がNaNならスキップ
        if pd.isna(row["MA5"]) or pd.isna(row["MA25"]) or pd.isna(row["RSI14"]) or pd.isna(row["Vol_ratio"]):
            continue

        # --- 新しいロジック ---
        cond_gc_after = row["GC_after"]              # GC発生後
        cond_uptrend = row["MA5_up"]                 # 上昇継続
        cond_pullback = close < row["MA5"]           # 押し目
        cond_rsi = row["RSI14"] <= 40                # RSI条件
        cond_vol = row["Vol_ratio"] >= 1.2           # 出来高条件

        if cond_gc_after and cond_uptrend and cond_pullback and cond_rsi and cond_vol:
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
    max_dd = trades_df["return"].cumsum().min() * 100

    print("===== バックテスト結果 =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%（累積リターンベース簡易）")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())
    print("\n--- トレード一覧（末尾10件） ---")
    print(trades_df.tail(10))
