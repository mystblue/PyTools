# -*- coding: utf-8 -*-

import json


def convert():
    json_obj = []
    monster = {}

    with open("monster.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            splitted = line.split('|')

            if len(splitted) == 8:
                # 新規
                monster = {}
                monster["名前"] = splitted[2]
                monster["弱点属性"] = splitted[6]
                act = {}
                act["状態"] = splitted[3]
                act["攻撃回数"] = splitted[4]
                act["タイプ"] = splitted[5]
                monster["行動"] = []
                monster["行動"].append(act)
                json_obj.append(monster)

            if len(splitted) == 7:
                # 他の状態
                act = {}
                act["状態"] = splitted[2]
                act["攻撃回数"] = splitted[3]
                act["タイプ"] = splitted[4]
                monster["行動"].append(act)
                pass

            print( "[" + line + "]")
            print(len(splitted))
    

    str = json.dumps(json_obj, ensure_ascii=False)
    with open("monster.js", "w", encoding="utf-8") as fw:
        fw.write(str)


if __name__ == '__main__':
    convert()
