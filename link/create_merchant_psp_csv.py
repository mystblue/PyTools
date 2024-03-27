# encoding: utf-8

"""
"""

import os

file_path = "merchant_psp_test_data.csv"

def main():
    book_list = []
    with open(file_path, "w", encoding="cp932", newline="\n") as fw:
        fw.write("内部管理ID,有効性,加盟店ID,加盟店名,決済代行事業者ID,決済代行事業者名,接続先環境ID,接続先環境名,決済代行事業者項目1,決済代行事業者項目2,決済代行事業者項目3,決済代行事業者項目4,決済代行事業者項目5,決済代行事業者項目6,決済代行事業者項目7,決済代行事業者項目8")
        fw.write('\n')
        for i in range(2000):
            ret = ",1," + str(45 + i) + ",テスト" + str(i + 1) + ",1,ベリトランス株式会社,test,試験,dummy,dummy"
            fw.write(ret)
            fw.write('\n')

if __name__ == '__main__':
    main()