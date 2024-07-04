# -*- coding: utf-8 -*-

import json

HTML = """            <div class="form-group">
                <label>{0}</label>
                <input type="text" name="{1}" class="form-control">
            </div>
"""

def outputFile(clist):
    ret = ""
    for item in clist:
        ret += HTML.format(item[1], item[0])
    with open("output.txt", "w", encoding="utf-8") as fp:
        fp.write(ret)

def main(file):
    ret_list = []
    with open(file, "r", encoding="utf-8") as fp:
        json_obj = json.load(fp)
        for method in json_obj:
            #print(method["key"])
            for item in method["request"]:
                print(item["key"])
                print(item["title"])
                ret = item["key"], item["title"]
                ret_list.append(ret)
        #print(json_obj)
    print(ret_list)
    clist = set(ret_list)
    print("---------")
    print(clist)
    outputFile(clist)

if __name__ == '__main__':
    main("sbps.json")
