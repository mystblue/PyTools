import openpyxl
from openpyxl import Workbook  # 「pip install openpyxl」でインストールしておく

name = "test.xlsx"

#Excelファイル読込
workbook = openpyxl.load_workbook(name)
sheet = workbook.active

#画像を選択
img_to_excel = openpyxl.drawing.image.Image("yamato\\28_001.png")

#指定の位置に画像を添付
sheet.add_image(img_to_excel, 'B3')

#保存
workbook.save(name)