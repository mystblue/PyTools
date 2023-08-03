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
    
    ret = []
    for test in json_obj:
        if "orderId" in test and test["orderId"] == "Veritrans_Dummy_02":
            ret.append(test)
        
    with open(output_file, "w", encoding="utf-8") as fw:
        fw.write(json.dumps(ret, ensure_ascii=False))

if __name__ == '__main__':
    test()
