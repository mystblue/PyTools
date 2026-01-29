import yfinance as yf
import pandas as pd
import ta  # pip install ta

# 1. 監視銘柄リスト
TICKERS = ["fujikura", "advantest", "ibiden", "lasertec", "sumco", "screen", "hoya", "rohm", "shinetsu", "tel", "furukawa", "denso", "shionogi", "chugai", "astellas", "nintendo", "capcom", "bandai", "kepco", "tepco", "enos", "mhi", "ihi", "khi", "itochu", "mitsubishi", "mitsui", "olc", "toyota", "nipponsteel", "jfeh", "nyk", "mol", "kilne", "kikkoman", "nipponham", "konami", "squareenix", "suzuki", "disco", "renesas", "softbankg", "ntt", "kddi", "softbank", "cyberagent", "rakuten", "zh", "fujitsu", "nec", "omron"]

def fetch_data(ticker):
    data = pd.read_csv("master\\" + ticker + ".csv")
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

def main():
    results = []

    for ticker in TICKERS:
        try:
            df = fetch_data(ticker)
            df = add_indicators(df)

            if len(df) < 25:
                continue

            today = df.iloc[-1]
            yesterday = df.iloc[-2]
            if is_buy_signal(today, yesterday):
                latest = df.iloc[-1]
                results.append({
                    "ticker": ticker,
                    "close": latest["Close"],
                    "rsi": latest["RSI14"],
                    "ma5": latest["MA5"],
                    "ma20": latest["MA20"],
                    "volume": latest["Volume"],
                })
        except Exception as e:
            print(f"Error for {ticker}: {e}")

    if results:
        df_res = pd.DataFrame(results)
        print("今日の買い候補：")
        print(df_res)
        df_res.to_csv("screening_results.csv", index=False)
    else:
        print("今日の条件合致銘柄はなし")

if __name__ == "__main__":
    main()