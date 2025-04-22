#coding:utf-8
import codecs
import sys

text = "2359401622896143"

def read_file():
    count = 0
    with codecs.open("all_databases_20220601.dump", "r", "utf-8", 'backslashreplace') as f:
        for line in f:
            if line.find(text) > 0:
                print(line)
                with open(text + ".txt", "w", encoding="utf-8") as fw:
                    fw.write(line)
                sys.exit()

if __name__ == '__main__':
    read_file()
