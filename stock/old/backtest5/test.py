import pandas as pd
import numpy as np

def compute_rsi(series, period: int = 14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def prepare_data(df: pd.DataFrame):
    """
    df: 日足データ
        必須列: Date, Open, High, Low, Close
    """
    df = df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date").set_index("Date")

    # 日足のSMA20
    df["SMA20"] = df["Close"].rolling(window=20, min_periods=20).mean()

    # 日足RSI
    df["RSI14"] = compute_rsi(df["Close"], period=14)

    # 週足にリサンプルしてSMA50, SMA100（終値ベース）
    weekly = df["Close"].resample("W-FRI").last()
    weekly_sma50 = weekly.rolling(window=50, min_periods=50).mean()
    weekly_sma100 = weekly.rolling(window=100, min_periods=100).mean()

    weekly_trend = pd.DataFrame({
        "weekly_sma50": weekly_sma50,
        "weekly_sma100": weekly_sma100
    })

    # 週足トレンドを日足に forward-fill で展開
    df = df.join(weekly_trend, how="left")
    df[["weekly_sma50", "weekly_sma100"]] = df[["weekly_sma50", "weekly_sma100"]].ffill()

    # 上昇トレンドフラグ
    df["up_trend"] = df["weekly_sma50"] > df["weekly_sma100"]

    return df


def backtest_high_winrate_rule(
    df: pd.DataFrame,
    tp_pct: float = 0.010,   # 利確 +1.0%
    sl_pct: float = 0.025,   # 損切り -2.5%
    rsi_low: float = 40.0,
    rsi_high: float = 50.0
):
    """
    勝率重視ルールのバックテスト
    戻り値: trades (DataFrame), equity_curve (Series)
    """
    df = prepare_data(df)

    position = 0  # 0: ノーポジ, 1: ロング
    entry_price = 0.0
    entry_date = None

    records = []

    equity = 1.0  # 初期資産を1.0とする（リターンのみ見る用）
    equity_curve = []

    for current_date, row in df.iterrows():
        open_price = row["Open"]
        high_price = row["High"]
        low_price = row["Low"]
        close_price = row["Close"]

        # 毎バーの資産推移（シンプルにクローズベースで更新）
        equity_curve.append((current_date, equity))

        # すでにポジションがある場合：利確 or 損切り判定
        if position == 1:
            tp_level = entry_price * (1 + tp_pct)
            sl_level = entry_price * (1 - sl_pct)

            exit_reason = None
            exit_price = None

            # 先に損切り・利確のヒット判定（ここはシンプルに順序固定）
            # 実運用に近づけるなら、ギャップや順序ロジックを調整してもOK
            if low_price <= sl_level:
                exit_price = sl_level
                exit_reason = "SL"
            elif high_price >= tp_level:
                exit_price = tp_level
                exit_reason = "TP"

            if exit_reason is not None:
                ret = (exit_price / entry_price) - 1
                equity *= (1 + ret)

                records.append({
                    "entry_date": entry_date,
                    "exit_date": current_date,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "return": ret,
                    "reason": exit_reason
                })

                position = 0
                entry_price = 0.0
                entry_date = None

                # ポジションを閉じたバーで新規エントリーはしない（シンプル化）
                continue

        # ノーポジならエントリー条件をチェック
        if position == 0:
            # 上昇トレンドでなければスキップ
            if not row["up_trend"]:
                continue

            # SMA20 が計算されていない期間はスキップ
            if np.isnan(row["SMA20"]) or np.isnan(row["RSI14"]):
                continue

            # 押し目条件：終値がSMA20付近（ここでは「SMA20より下に一度押してから反発した」とみなす簡易版）
            # ここでは「前日まではSMA20より下 or 近辺、当日陽線で反発」というイメージ
            prev_row = df.shift(1).loc[current_date]
            if np.isnan(prev_row["SMA20"]) or np.isnan(prev_row["RSI14"]):
                continue

            # 陽線判定
            bullish_candle = close_price > open_price

            # SMA20 付近への押し（前日CloseがSMA20以下、当日CloseがSMA20以上 or 近辺）
            touched_sma20 = (prev_row["Close"] <= prev_row["SMA20"]) and (close_price >= row["SMA20"] * 0.995)

            # RSIゾーン
            rsi_cond = (row["RSI14"] >= rsi_low) and (row["RSI14"] <= rsi_high)

            if bullish_candle and touched_sma20 and rsi_cond:
                position = 1
                entry_price = close_price  # 終値でエントリーと仮定
                entry_date = current_date

    # DataFrame化
    trades = pd.DataFrame(records)
    equity_curve = pd.Series(
        [e for _, e in equity_curve],
        index=[d for d, _ in equity_curve],
        name="equity"
    )

    return trades, equity_curve


# 例: CSVから日足データを読み込んでバックテスト
#df = pd.read_csv("..\\..\\master\\appier.csv")  # Date, Open, High, Low, Close
#df = pd.read_csv("..\\..\\master\\fujikura.csv")  # Date, Open, High, Low, Close
df = pd.read_csv("..\\..\\master\\nec.csv")  # Date, Open, High, Low, Close

trades, equity = backtest_high_winrate_rule(
    df,
    tp_pct=0.010,   # 利確 +1.0%
    sl_pct=0.025,   # 損切り -2.5%
    rsi_low=40.0,
    rsi_high=50.0
)

print(trades.head())
print("トレード数:", len(trades))
print("勝率:", (trades["return"] > 0).mean())
print("最終リターン:", equity.iloc[-1] - 1)

print("\n--- トレード一覧（末尾10件） ---")
print(trades.tail(10))