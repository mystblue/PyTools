# -*- coding: utf-8 -*-

# エビデンスの画像をエクセル形式でまとめる

import openpyxl
from openpyxl import Workbook

device_list = ["Pay TG PC アプリケーション", "Smart TG PC アプリケーション", "Smart TG スタンドアロン"]

check_list = [("デビットカード", "カード番号：4001420000000000"), ("プリペイドカード", "カード番号：4063190000000000")]

input_methods = [
     ("カード預かり登録", "以下のカード番号でカード預かり登録を行う", "GW エラーとなり、「入力されたカード番号はデビットカード/プリペイドカードのため、ご利用いただくことができません。クレジットカードのご利用をお願いします。」というメッセージが表示されること"),
     ("カード預かり更新", "以下のカード番号でカード預かり更新を行う", "GW エラーとなり、「入力されたカード番号はデビットカード/プリペイドカードのため、ご利用いただくことができません。クレジットカードのご利用をお願いします。」というメッセージが表示されること"),
]


content = "全パラメータをバリデーションルールに従って入力し、決済が正常に終了すること"

message = "取引履歴に記録されていることを確認する"

def do_loop(ws):
    num = 14

    for device in device_list:
        for check in check_list:
            for input_method in input_methods:
                title = "ペイジェント デビット／プリペイド判定\n" + device + "\n" + "　" + check[0] + "\n　" + input_method[0]
                ws["C" + str(num)] = title
                ws["I" + str(num)] = "正常系"
                ws["S" + str(num)] = input_method[1] + "\n" + check[1]
                ws["AI" + str(num)] = input_method[2]
                num += 1

def report():
    wb = openpyxl.load_workbook("test.xlsx")
    ws = wb['決済']  # ワークシートを指定
    ws = wb.active  # アクティブなワークシートを選択
    
    do_loop(ws)

    #ws["C14"] = "test"
    #ws["I14"] = "正常系"
    #ws["Q14"] = "test1"
    #ws["AA14"] = "test2"

    wb.save('test.xlsx')

if __name__ == '__main__':
    report()
