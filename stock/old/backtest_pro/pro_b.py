import pandas as pd
import numpy as np

# =========================
# 設定
# =========================
#CSV_PATH = "price_data.csv"   # 日足データ: Date, Open, High, Low, Close, Volume
CSV_PATH = "..\\..\\master\\fujikura.csv"  # 日足データのCSVパス
DONCHIAN_ENTRY = 20           # エントリー用ドンチャン期間（高値）
DONCHIAN_EXIT = 10            # エグジット用ドンチャン期間（安値）
SMA_LONG = 300                # 長期トレンド判定用SMA
ATR_PERIOD = 14               # ATR期間
ATR_MULTIPLIER = 3            # ATRトレーリング倍率

# =========================
# ATR計算
# =========================
def compute_atr(df, period=14):
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift(1)).abs()
    low_close = (df["Low"] - df["Close"].shift(1)).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

# =========================
# インジケーター計算
# =========================
def compute_indicators(df):
    df["SMA_LONG"] = df["Close"].rolling(SMA_LONG).mean()
    df["DC_HIGH"] = df["High"].rolling(DONCHIAN_ENTRY).max()
    df["DC_LOW"] = df["Low"].rolling(DONCHIAN_EXIT).min()
    df["ATR"] = compute_atr(df, ATR_PERIOD)
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
position = None  # {"entry_date":..., "entry_price":..., "atr_stop":...}

for i in range(1, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i - 1]

    date = row["Date"]
    close = row["Close"]

    # 必要な指標がNaNならスキップ
    if pd.isna(row["SMA_LONG"]) or pd.isna(row["DC_HIGH"]) or pd.isna(row["DC_LOW"]) or pd.isna(row["ATR"]):
        continue

    # =========================
    # エグジット（ATRトレーリング or Donchian10割れ）
    # =========================
    if position is not None:
        entry_price = position["entry_price"]
        atr_stop = position["atr_stop"]

        # ATRトレーリング更新（高値更新時）
        new_stop = close - row["ATR"] * ATR_MULTIPLIER
        atr_stop = max(atr_stop, new_stop)
        position["atr_stop"] = atr_stop

        # ATRストップ割れ
        if close < atr_stop:
            ret = (close - entry_price) / entry_price
            trades.append({
                "entry_date": position["entry_date"],
                "entry_price": entry_price,
                "exit_date": date,
                "exit_price": close,
                "return": ret,
                "reason": "ATR_trailing",
            })
            position = None
            continue

        # Donchian10割れ
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
            continue

    # =========================
    # エントリー（SMA300上＆Donchian20高値ブレイク）
    # =========================
    if position is None:
        cond_trend = close > row["SMA_LONG"]
        cond_breakout = (prev["Close"] <= prev["DC_HIGH"]) and (close > row["DC_HIGH"])

        if cond_trend and cond_breakout:
            atr_stop = close - row["ATR"] * ATR_MULTIPLIER
            position = {
                "entry_date": date,
                "entry_price": close,
                "atr_stop": atr_stop,
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

    equity_curve = (1 + trades_df["return"]).cumprod()
    peak = equity_curve.cummax()
    dd_series = (equity_curve / peak - 1) * 100
    max_dd = dd_series.min()

    print("===== プロ仕様 Donchian × SMA300 × ATRトレーリング =====")
    print(f"総トレード数      : {total_trades}")
    print(f"勝率              : {win_rate:.2f}%")
    print(f"平均リターン      : {avg_ret:.2f}% / トレード")
    print(f"平均勝ちトレード  : {avg_win:.2f}%")
    print(f"平均負けトレード  : {avg_loss:.2f}%")
    print(f"累積リターン      : {cum_ret*100:.2f}%")
    print(f"最大ドローダウン  : {max_dd:.2f}%")

    print("\n--- トレード一覧（先頭5件） ---")
    print(trades_df.head())