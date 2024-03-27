# encoding: utf-8

"""
"""

import os

file_path = "merchant_test_data.csv"

def main():
    book_list = []
    with open(file_path, "w", encoding="cp932", newline="\n") as fw:
        fw.write("内部管理ID,登録日時,加盟店コード,契約開始日,解約日,加盟店名,備考")
        fw.write('\n')
        for i in range(2000):
            ret = ",2024/03/27 09:20,test" + "{:06d}".format(i + 1) + ",2022-10-10,,テスト" + str(i + 1) + ","
            fw.write(ret)
            fw.write('\n')

if __name__ == '__main__':
    main()