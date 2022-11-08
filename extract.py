# -*- coding: utf-8 -*-

import json
import os
import sys

file_path = "veritrans_test.json"

output_file = "veritrans_test_group.json"

error_no = "error_no.txt"

error_list = []

def test():
    buf = ""
    with open(file_path, "r", encoding="utf-8") as f:
        buf = f.read()
    json_obj = json.loads(buf)

    with open(error_no, "r", encoding="utf-8") as f:
        for line in f:
            str = line.rstrip('\r\n')
            error_list.append(str)
    
    ret = []
    for test in json_obj:
        if test["testNo"] in error_list:
            ret.append(test)
        
    with open(output_file, "w", encoding="utf-8") as fw:
        fw.write(json.dumps(ret, ensure_ascii=False))

if __name__ == '__main__':
    test()
