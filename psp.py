# coding: utf-8

psp_list = ["DGFT", "ソニーペイメント", "ペイジェント", "GMO-PG", "SMBCファイナンス", "ヤマトフィナンシャル", "ゼウス", "SMBC-GMO", "GMO-MG", "三菱UFGニコス", "NTTコムオンライン"]

file_path = "psp.txt"

def main():
    with open(file_path, "w", encoding="utf-8") as f:
        for psp in psp_list:
            str = '' + psp + "\n（表示項目すべて非表示）\n"
            str += '' + psp + "\n（表示項目すべて表示）\n"
            str += '' + psp + "\n（オーソリのみ）\n"
            f.write(str)

if __name__ == '__main__':
    main()
