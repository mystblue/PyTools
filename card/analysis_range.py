#coding:utf-8
import codecs
import sys

text1 = "2221060511310693"
text2 = "4820060711334809"

def read_file():
    count = 0
    output = False
    exit = False
    with codecs.open("all_databases_20220601.dump", "r", "utf-8", 'backslashreplace') as f:
        with open("sp.txt", "w", encoding="utf-8") as fw:
            for line in f:
                if exit:
                    sys.exit()
                if line.find(text1) > 0:
                    output = True
                if line.find(text2) > 0:
                    exit = True
                if output:
                    fw.write(line)

if __name__ == '__main__':
    read_file()
