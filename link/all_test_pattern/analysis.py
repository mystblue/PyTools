# -*- coding: utf-8 -*-

import json

# PSP 固有のフィールド

psp = "paygent"


# psp の json ファイルを読み込む
def read_json(psp):
    file_path = psp + ".json"
    with open(file_path, "r", encoding="utf-8") as fp:
        json_obj = json.load(fp)
    return json_obj

# json ファイルを解析して、以下のようなデータ構造を作る
"""
    [
        {
            "オーソリ",
            [
                {
                    "顧客ID",
                    "任意／非表示|任意／表示／空白|任意／表示／あり"
                }
            ]
        },
    ]
"""
def create_date_structure(json_obj):
    data = []
    
    for transaction_type in json_obj:
        dic = {}
        print(transaction_type["key"])
        item_list = []
        for request in transaction_type["request"]:
            #print(request["title"])
            
            title = request["title"]
            index = title.find("(")
            if index > 0:
                title = title[:index]
            
            if "choice" in request:
                # choice
                param = {}
                p = ""
                for c in request["choice"]:
                    p += c["title"] + "|"
                p = p[:-1]
                param[title] = p
                item_list.append(param)
            elif request["isRequired"]:
                print("必須")
                # 必須
                param = {}
                param[title] = "必須"
                item_list.append(param)
            else:
                param = {}
                if title == "マーチャントID" or request["title"] == "サイトID":
                    param[title] = "|任意／あり|任意／なし"
                else:
                    param[title] = "任意／非表示|任意／表示／空白|任意／表示／あり"
                item_list.append(param)
        t_type = transaction_type["key"]
        dic[t_type] = item_list
        data.append(dic)
    return data

def create_header(data):
    data_set = []
    for transaction_type in data:
        keys = transaction_type.keys()
        for key in keys:
            #print(transaction_type[key])
            for item in transaction_type[key]:
                ckeys = item.keys()
                for ckey in ckeys:
                    if not ckey in data_set:
                        if not ckey == "マーチャントID" and not ckey == "サイトID":
                            data_set.append(ckey)
    data_set.append("マーチャントID")
    data_set.append("サイトID")
    return data_set

def get_first_key(dic):
    keys = dic.keys()
    for key in keys:
        return key
    return None

def normalize(data_set, data):
    new_data = []
    for transaction_type in data:
        dic = {}
        item_list = []
        deal_type = get_first_key(transaction_type)
        for param in data_set:
            param_found = False
            for p in transaction_type[deal_type]:
                if param in p:
                    item_list.append(p)
                    param_found = True
            if not param_found:
                p = {}
                p[param] = "非表示"
                item_list.append(p)
        dic[deal_type] = item_list
        new_data.append(dic)
    return new_data

def main():
    json_obj = read_json(psp)
    data = create_date_structure(json_obj)
    print(data)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    
    # データの標準化
    data_set = create_header(data)
    #print(data_set)
    data = normalize(data_set, data)
    
    with open(psp + "_data.json", "w", encoding="utf-8") as fp:
        fp.write(json.dumps(data, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
