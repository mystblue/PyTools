import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

# ===== パラメータ =====
#TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "appier", "sumco", "screen", "hoya", "rohm", "kokusai", "shinetsu", "tel"]
TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "sumco", "screen", "hoya", "rohm", "shinetsu", "tel", "furukawa", "denso", "shionogi", "chugai", "astellas", "nintendo", "capcom", "bandai", "kepco", "tepco", "enos", "mhi", "ihi", "khi", "itochu", "mitsubishi", "mitsui", "olc", "toyota", "nipponsteel", "jfeh", "nyk", "mol", "kilne", "kikkoman", "nipponham", "konami", "squareenix", "suzuki", "subaru", "disco", "renesas", "softbankg", "ntt", "kddi", "softbank", "cyberagent", "rakuten", "zh", "fujitsu", "nec", "omron"]
START = "2016-01-28"
END = None  # None なら最新まで

def fetch_data(ticker):
    data = pd.read_csv(ticker + "_10y.csv")

    return data

# ===== テクニカル付与 =====
def calc_rsi(series, period=14):
    diff = series.diff()
    up = diff.clip(lower=0)
    down = -diff.clip(upper=0)

    gain = up.rolling(period).mean()
    loss = down.rolling(period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_indicators(df, bb_window=20, bb_sigma=2, rsi_period=14):
    # RSI
    df["RSI14"] = calc_rsi(df["Close"], period=rsi_period)

    # ボリンジャーバンド（終値ベース）
    ma = df["Close"].rolling(bb_window).mean()
    std = df["Close"].rolling(bb_window).std()

    df["BB_MID"] = ma
    df["BB_UPPER"] = ma + bb_sigma * std
    df["BB_LOWER"] = ma - bb_sigma * std

    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA75"] = df["Close"].rolling(75).mean()
    df["MA75_SLOPE"] = df["MA75"].diff()

    return df

# ===== 改善後ルール：買いシグナル判定（その日の終値ベース） =====
def is_buy_signal(latest, prev):
    """
    - RSI30以下 → 反転で買い
    - ボリンジャーバンド -2σ → 内側に戻ったら買い
    - 連続陰線（3〜5日）→ 陽線で反転
    """
    
    # --- 暴落フィルター（MA75の傾き） ---
    if latest["MA75_SLOPE"] <= 0:
        return False
    
    # ---------- 1. RSI30以下 → 反転で買い ----------
    rsi_cond = (
        (prev["RSI14"] < 30) and
        (latest["RSI14"] > prev["RSI14"])  # 反転（RSIが上向き）
    )

    # ---------- 2. BB -2σ → 内側に戻ったら買い ----------
    # 前日が -2σ の外（下）で、当日が -2σ の内側に戻る
    bb_cond = (
        (prev["Close"] < prev["BB_LOWER"]) and
        (latest["Close"] > latest["BB_LOWER"])
    )
    """
    # ---------- 3. 連続陰線（3〜5日）→ 陽線で反転 ----------
    # 直近の「連続陰線日数」をカウント（最新日の1日前まで）
    consec_down = 0
    for i in range(2, 7):  # 最大5本分さかのぼる（-2, -3, -4, -5, -6）
        if len(df) - i - 1 < 0:
            break
        cur = df.iloc[-i]
        prev_candle = df.iloc[-i - 1]
        if cur["Close"] < prev_candle["Close"]:
            consec_down += 1
        else:
            break
    # 3〜5日連続陰線 ＋ 当日が陽線（反転）
    consec_cond = (
        (3 <= consec_down <= 5) and
        (latest["Close"] > latest["Open"])  # 陽線
    )
    """

    # いずれかの逆張り条件を満たせば買いシグナル
    return rsi_cond or bb_cond

# ===== 売りシグナル（20MA割れ） =====
def is_sell_signal(daily_row_prev, daily_row):
    return (daily_row_prev["Close"] >= daily_row_prev["MA20"]) and (daily_row["Close"] < daily_row["MA20"])

def max_drawdown(equity):
    s = pd.Series(equity)
    peak = s.cummax()
    dd = (s - peak) / peak
    return dd.min()

# ===== 1銘柄バックテスト =====
def backtest_single(ticker):
    print(f"=== Backtest: {ticker} ===")
    equity = [1.0]   # 初期資産を1.0とする

    data = fetch_data(ticker)

    if len(data) < 200:
        print("データ不足")
        return None

    data = add_indicators(data)

    # 欠損除去
    data = data.dropna()

    position = 0  # 0: ノーポジ, 1: ロング
    entry_price = 0.0
    trades = []

    # 日足を1本ずつ進める（翌日の始値で約定する前提）
    for i in range(21, len(data) - 1):
        today = data.iloc[i]
        #print(today)
        yesterday = data.iloc[i - 1]
        tomorrow = data.iloc[i + 1]  # 約定価格用

        # 売り判定（ポジションありのとき）
        if position == 1 and is_sell_signal(yesterday, today):
            exit_price = tomorrow["Open"]
            pl = exit_price - entry_price
            equity.append(equity[-1] * (1 + pl / entry_price))
            #print(today)
            #print("利益 = " + str(exit_price) + " - " + str(entry_price))
            #print(pl)
            trades.append(pl)
            position = 0
            entry_price = 0.0

        # 買い判定（ノーポジのとき）
        if position == 0 and is_buy_signal(today, yesterday):
            #print(today)
            entry_price = tomorrow["Open"]
            position = 1

    # 最後までポジションが残っていたら、最終日の終値でクローズ
    if position == 1:
        last_close = data.iloc[-1]["Close"]
        pl = last_close - entry_price
        equity.append(equity[-1] * (1 + pl / entry_price))
        #print(today)
        #print("利益 = " + str(last_close) + " - " + str(entry_price))
        #print(pl)
        trades.append(pl)

    if len(trades) == 0:
        print("トレードなし")
        return {
            "ticker": ticker,
            "trades": 0,
            "win_rate": None,
            "total_pl": 0.0,
            "avg_pl": None,
        }

    wins = [t for t in trades if t > 0]
    win_rate = len(wins) / len(trades)
    total_pl = sum(trades)
    avg_pl = total_pl / len(trades)

    wins2 = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]

    total_profit = sum(wins2)
    total_loss = abs(sum(losses)) if losses else 0.0

    # 
    pf = total_profit / total_loss if total_loss > 0 else float("inf")
    
    # 最大ドローダウン
    dd = max_drawdown(equity)


    result = {
        "ticker": ticker,
        "trades": len(trades),
        "win_rate": win_rate,
        "total_pl": total_pl,
        "avg_pl": avg_pl,
        "pf": pf,
        "dd": dd,
    }
    print(result)
    return result

# ===== 複数銘柄まとめてバックテスト =====
def main():
    results = []
    for ticker in TICKERS:
        res = backtest_single(ticker)
        if res is not None:
            results.append(res)

    if not results:
        print("結果なし")
        return

    df = pd.DataFrame(results)
    print("\n=== Summary ===")
    print(df)

    print("\n平均勝率:", df["win_rate"].mean())
    print("合計損益:", df["total_pl"].sum())
    print("平均損益/トレード:", df["avg_pl"].mean())
    print("プロフィットファクター:", df["pf"].mean())
    print("平均DD:", df["dd"].mean())

if __name__ == "__main__":
    main()