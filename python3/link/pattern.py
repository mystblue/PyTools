# -*- coding: utf-8 -*-

import os
import sys

file_path = "testResult_20220705100001.csv"

def test():
    buf = ""
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            splitted = line.split(",")
            length = len(splitted)
            if splitted[2] == "NG":
                buf += splitted[1] + "\n"
    
    with open("erro_no.txt", "w", encoding="utf-8") as fw:
        fw.write(buf)

if __name__ == '__main__':
    test()
