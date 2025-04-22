# -*- coding: utf-8 -*-

import os
import sys

file_path = "ccsrch_20220613.log"

def test():
    buf = ""
    pre = ""
    count = 0
    list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            splitted = line.split("\t")
            length = len(splitted)
            card_no = splitted[length - 1][:-1]
            if not card_no in list:
                list.append(card_no)
    
    with open("num_all.txt", "w", encoding="utf-8") as fw:
        fw.write(str(len(list)))

if __name__ == '__main__':
    test()
