# encoding: utf-8

"""
"""

import json
import os

file_path = "sendtestdata_test.json"

def main():
    buf = ""
    with open(file_path, "r", encoding="utf-8") as f:
        buf = f.read()
    json_obj = json.loads(buf)
    
    result = []
    
    sns = set()
    
    for obj in json_obj:
        result.append(obj["header"]["SN"] + " -> " + obj["request"]["pspShortName"])
        sns.add(obj["header"]["SN"])

    result.sort()
    
    for item in result:
        print(item)

    print("---")

    # 79 - 12 = 67 - 5 = 62

    print(str(len(sns)))

    for sn in sns:
        print(sn)


if __name__ == '__main__':
    main()