# -*- coding: utf-8 -*-

import json

# PSP 固有のフィールド

psp = "paygent"


# psp の json ファイルを読み込む
def read_json(psp):
    file_path = psp + "_test.json"
    with open(file_path, "r", encoding="utf-8") as fp:
        json_obj = json.load(fp)
    return json_obj

def main():
    json_obj = read_json(psp)
    print("■合計 = " + str(len(json_obj)))
    
    success = 0
    failure = 0
    
    dic = {}
    dic_e = {}
    
    for data in json_obj:
        if data["区分"] == "正常系":
            success = success + 1
            category = data["処理区分"]
            if category in dic:
                dic[category] = dic[category] + 1
            else:
                dic[category] = 1
        elif data["区分"] == "異常系":
            failure = failure + 1
            category = data["処理区分"]
            if category in dic_e:
                dic_e[category] = dic_e[category] + 1
            else:
                dic_e[category] = 1
    
    print("■正常系 = " + str(success))
    
    keys = dic.keys()
    for key in dic:
        print("■" + key + " = " + str(dic[key]))

    print("■異常系 = " + str(failure))
    keys = dic_e.keys()
    for key in dic_e:
        print("■" + key + " = " + str(dic_e[key]))

if __name__ == '__main__':
    main()
