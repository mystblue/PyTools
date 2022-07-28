# -*- coding: utf-8 -*-

# エビデンスの画像をエクセル形式でまとめる

import math
import openpyxl
from openpyxl import Workbook
import os
from PIL import Image

folder = 'test'

def search_dir(ws):
    folders = os.listdir(folder)
    count = 2
    pre_test_no = ''
    for file_name in folders:
        test_no = file_name.split('_')[0]
        
        if pre_test_no != test_no:
            ws['B' + str(count)] = "No. " + test_no
            count += 2
            pre_test_no = test_no
        
        # 画像を張り付け
        file_path = folder + '\\' + file_name
        im = Image.open(file_path)
        w, h = im.size
        
        img_to_excel = openpyxl.drawing.image.Image(file_path)
        #指定の位置に画像を添付
        ws.add_image(img_to_excel, 'B' + str(count))
        count += math.ceil(h / 17) + 2


def report():
    # ワークブックの新規作成と保存
    wb = Workbook()
    ws = wb['Sheet']  # ワークシートを指定
    ws = wb.active  # アクティブなワークシートを選択
    
    # ディレクトリ以下の画像をサーチ
    search_dir(ws)
    
    wb.save('myworkbook.xlsx')

if __name__ == '__main__':
    report()
