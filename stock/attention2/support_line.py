import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def fetch_data_local(filepath):
    data = pd.read_csv(filepath)
    return data

def find_support_lines(df, order=5, tolerance=0.002):
    """
    df: 日足データ（カラム: 'Low' 必須）
    order: 局所安値を検出する際の期間
    tolerance: 水平線としてまとめる許容誤差（0.002 = 0.2%）
    """

    # 局所安値（ローカルミニマム）を抽出
    local_mins_idx = argrelextrema(df['Low'].values, np.less_equal, order=order)[0]
    local_mins = df.iloc[local_mins_idx][['Date', 'Low']]

    # クラスター化してサポートライン候補を抽出
    support_lines = []
    cluster = []

    for _, row in local_mins.iterrows():
        price = row['Low']

        if not cluster:
            cluster = [price]
            continue

        # クラスター内の平均値と比較して許容範囲内なら同じ水平線とみなす
        if abs(price - np.mean(cluster)) / np.mean(cluster) <= tolerance:
            cluster.append(price)
        else:
            support_lines.append(np.mean(cluster))
            cluster = [price]

    # 最後のクラスターも追加
    if cluster:
        support_lines.append(np.mean(cluster))

    # 価格の低い順に並べる
    support_lines = sorted(support_lines)

    return support_lines, local_mins


if __name__ == '__main__':
    df = fetch_data_local("..\\master\\konami.csv")
    support_lines, local_mins = find_support_lines(df)
    
    print("サポートライン候補:")
    for line in support_lines:
        print(f"{line:.2f} 円")
