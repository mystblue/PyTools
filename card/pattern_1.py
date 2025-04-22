# -*- coding: utf-8 -*-

import os
import sys

file_path = "ccsrch_20220613.log"

def test():
    buf = ""
    pre = ""
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            splitted = line.split("\t")
            length = len(splitted)
            card_no = splitted[length - 1][:-1]
            if card_no == pre:
                count += 1
            else:
                if count == 1:
                    buf += '  "' + pre + '",\n' 
                count = 1
                pre = card_no
        if count == 1:
            buf += '  "' + card_no + '",\n'
    
    with open("num1.txt", "w", encoding="utf-8") as fw:
        fw.write(buf)

if __name__ == '__main__':
    test()
