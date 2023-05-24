# -*- coding: utf-8 -*-
import csv
import json
import requests
import pprint

def main():

    payload = {
        'apiKey': 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf',   # xxxxx は API キーを設定
        'projectId[]': ['111745'],
        'milestoneId[]': ['373344'],
        'count': 100,
        'order': 'asc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # curl https://pcidss.backlog.jp/api/v2/issues/PTG_DEV-409/comments?apiKey=FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf
    issues = requests.get('https://pcidss.backlog.jp/api/v2/issues/PTG_DEV-409/attachments?count=100&apiKey=' + 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf', headers = headers) # xxxxx は環境にあわせて設定

    #print(issues)
    #pprint.pprint(issues.json())
    #print(issues.json())
    with open("result_409_a.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(issues.json()))

def main2():
    buf = ""
    with open("result_409_a.json", "r", encoding="utf-8") as f:
        buf = f.read()

    json_obj = json.loads(buf)
    print(len(json_obj))
    
    for item in json_obj:
        print(item['id'])
        print(item['name'])
    #    print(item['status']['name'])

if __name__ == '__main__':
    main()
    main2()
    