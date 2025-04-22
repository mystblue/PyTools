# -*- coding: utf-8 -*-

import os
import sys

file_path = "ccsrch_20220613.log"

def check_number(digits):
    _sum = 0
    alt = False
    for dg in reversed(digits):
        d = int(dg)
        assert 0 <= d <= 9
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        _sum += d
        alt = not alt
    return (_sum % 10) == 0

def test():
    list = []
    ng_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            splitted = line.split("\t")
            length = len(splitted)
            card_no = splitted[length - 1][:-1]
            if not card_no in list:
                if check_number(card_no):
                    list.append(card_no)
                else:
                    ng_list.append(card_no)
    
    with open("num_all.txt", "w", encoding="utf-8") as fw:
        fw.write(str(len(list)))

if __name__ == '__main__':
    test()
