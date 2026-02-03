import pandas as pd
import numpy as np

# =========================================================
# データ読み込み（例：Date, Open, High, Low, Close, Volume）
# =========================================================
def load_price(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").set_index("Date")
    return df


# =========================================================
# RSI 計算
# =========================================================
def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    diff = series.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)

    gain = up.ewm(alpha=1/period, adjust=False).mean()
    loss = down.ewm(alpha=1/period, adjust=False).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# =========================================================
# 週足トレンド判定（20MA 上向き & 終値 > 20MA で上昇トレンド）
# =========================================================
def add_weekly_trend(daily: pd.DataFrame) -> pd.DataFrame:
    # 週足にリサンプル
    weekly = daily.resample("W-FRI").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    weekly["MA20"] = weekly["Close"].rolling(20).mean()
    weekly["MA20_slope"] = weekly["MA20"] - weekly["MA20"].shift(1)
    weekly["trend_up"] = (weekly["MA20_slope"] > 0) & (weekly["Close"] > weekly["MA20"])

    # 週足トレンドを日足に forward fill で付与
    trend = weekly[["trend_up"]].reindex(daily.index, method="ffill")
    daily = daily.copy()
    daily["trend_up"] = trend["trend_up"].fillna(False)
    return daily


# =========================================================
# 日足インジケータ（MA, ボリンジャー, RSI）
# =========================================================
def add_daily_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA20_SLOPE"] = df["MA20"].diff()

    # ボリンジャーバンド（20期間）
    period_bb = 20
    df["BB_MID"] = df["Close"].rolling(period_bb).mean()
    df["BB_STD"] = df["Close"].rolling(period_bb).std()
    df["BB_UP"] = df["BB_MID"] + 2 * df["BB_STD"]
    df["BB_LOW"] = df["BB_MID"] - 2 * df["BB_STD"]

    # RSI
    df["RSI"] = calc_rsi(df["Close"], period=14)

    df["VOLUME_MA20"] = df["Volume"].rolling(window=20).mean()

    return df


# =========================================================
# シグナル生成（順張り＋押し目＋反転確認）
# =========================================================
def generate_long_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 押し目条件（RSI 30〜45 & MA5 or MA10 付近 & 陰線）
    rsi_pullback = (df["RSI"] >= 35) & (df["RSI"] <= 55)

    ma_touch = (
        (abs(df["Close"] - df["MA5"]) / df["Close"] < 0.01) |
        (abs(df["Close"] - df["MA10"]) / df["Close"] < 0.01)
    )

    bearish_candle = df["Close"] < df["Open"]

    prev_close2 = df["Close"].shift(1)
    my = df["Close"] < prev_close2

    pullback = rsi_pullback & ma_touch & bearish_candle & my

    # 反転シグナル（陽線包み足 or RSI 上向き or MA5 上抜け）
    bullish_candle = df["Close"] > df["Open"]
    prev_close = df["Close"].shift(1)
    prev_open = df["Open"].shift(1)

    engulfing = bullish_candle & (df["Close"] > prev_open) & (df["Open"] < prev_close)

    rsi_turn_up = (df["RSI"] > df["RSI"].shift(1))

    ma5_cross_up = (df["Close"] > df["MA5"]) & (df["Close"].shift(1) <= df["MA5"].shift(1))

    vol_ok = df["Volume"] > df["VOLUME_MA20"]

    reversal = engulfing | rsi_turn_up | ma5_cross_up | vol_ok

    # 週足トレンドが上昇 & 押し目後の反転でロングエントリー
    df["long_entry"] = df["trend_up"] & pullback.shift(1) & reversal

    return df


# =========================================================
# シンプルな R ベース・バックテスト
#   - 損切り：エントリー価格の 2% 下
#   - 利確：1.5R（= 3% 上）
# =========================================================
def backtest_long_R(df: pd.DataFrame,
                    stop_pct: float = 0.05,
                    reward_R: float = 1.2) -> pd.DataFrame:
    df = df.copy()
    trades = []

    in_position = False
    entry_price = None
    stop_price = None
    target_price = None
    entry_date = None

    for date, row in df.iterrows():
        price = row["Close"]

        # エントリー判定
        if (not in_position) and row.get("long_entry", False):
            print("■買った日")
            print(date)
            in_position = True
            entry_price = price
            entry_date = date

            risk_price = entry_price * stop_pct
            stop_price = entry_price - risk_price
            target_price = entry_price + risk_price * reward_R
            continue

        # ポジション保有中の決済判定
        if in_position:
            low = row["Low"]
            high = row["High"]

            exit_reason = None
            exit_price = None

            # 先に損切りヒット判定
            if low <= stop_price:
                print("■損切り日："+ str(price - entry_price))
                print(date)
                exit_price = stop_price
                exit_reason = "SL"
            # 次に利確ヒット判定
            elif high >= target_price:
                print("■売った日：" + str(target_price - entry_price))
                print(date)
                exit_price = target_price
                exit_reason = "TP"

            if exit_price is not None:
                R = (exit_price - entry_price) / (entry_price * stop_pct)

                trades.append({
                    "entry_date": entry_date,
                    "exit_date": date,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "R": R,
                    "reason": exit_reason
                })

                in_position = False
                entry_price = stop_price = target_price = None
                entry_date = None

    trades_df = pd.DataFrame(trades)
    return trades_df


# =========================================================
# 集計
# =========================================================
def summarize_trades(trades: pd.DataFrame):
    if trades.empty:
        print("トレードなし")
        return

    win = trades[trades["R"] > 0]
    lose = trades[trades["R"] <= 0]

    win_rate = len(win) / len(trades) if len(trades) > 0 else 0
    avg_win = win["R"].mean() if not win.empty else 0
    avg_lose = lose["R"].mean() if not lose.empty else 0
    expectancy = win_rate * avg_win + (1 - win_rate) * avg_lose

    print("総トレード数:", len(trades))
    print("勝率:", round(win_rate * 100, 2), "%")
    print("平均勝ち(R):", round(avg_win, 3))
    print("平均負け(R):", round(avg_lose, 3))
    print("期待値(R):", round(expectancy, 3))


# =========================================================
# メイン例
# =========================================================
if __name__ == "__main__":
    # 例：'prices.csv' を読み込んで実行
    df = load_price("..\\..\\master\\lasertec.csv")
    #df = load_price("..\\..\\master\\mol.csv")

    df = add_weekly_trend(df)
    df = add_daily_indicators(df)
    df = generate_long_signals(df)

    trades = backtest_long_R(df,
                             stop_pct=0.05,   # 1回のリスク 2%
                             reward_R=1.2)    # 利確 1.5R

    summarize_trades(trades)

    # 必要なら trades.to_csv("trades_result.csv", index=False)