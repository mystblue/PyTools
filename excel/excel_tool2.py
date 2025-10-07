# -*- coding: utf-8 -*-

# エビデンスの画像をエクセル形式でまとめる

import openpyxl
from openpyxl import Workbook

def do_loop(ws):

    #num = 5
    for num in range(3, 332):
        ws["M" + str(num)] = "=XLOOKUP(LEFT(L" + str(num) + ",3), マスタ!B1:B47, マスタ!C1:C47, \"見つかりません\", 0)"

def report():
    wb = openpyxl.load_workbook("SIM不良対象リスト_202510_サマリ1.xlsx")
    ws = wb['リンク様_SIM不良対象リスト']  # ワークシートを指定
    ws = wb.active  # アクティブなワークシートを選択
    
    do_loop(ws)

    wb.save('SIM不良対象リスト_202510_サマリ1_第二集計.xlsx')

if __name__ == '__main__':
    report()
