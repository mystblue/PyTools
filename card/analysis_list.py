#coding:utf-8
import codecs
import sys

list = [
  "4921062115277004",
  "4921062118069697"
];

def read_file():
    count = 0
    text = list[count]
    with codecs.open("all_databases_20220601.dump", "r", "utf-8", 'backslashreplace') as f:
        for line in f:
            if line.find(text) > 0:
                print(line)
                with codecs.open(text + ".txt", "w", "utf-8") as fw:
                    fw.write(line)
                count += 1
                if count < len(list):
                    text = list[count]
                else:
                    sys.exit()

if __name__ == '__main__':
    read_file()
