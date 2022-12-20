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
    issues = requests.get('https://pcidss.backlog.jp/api/v2/issues?apiKey=' + 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf', data = payload, headers = headers) # xxxxx は環境にあわせて設定

    #print(issues)
    #pprint.pprint(issues.json())
    #print(issues.json())
    with open("result.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(issues.json()))

def main2():
    buf = ""
    with open("result.json", "r", encoding="utf-8") as f:
        buf = f.read()

    json_obj = json.loads(buf)
    print(len(json_obj))
    
    for item in json_obj:
        print(item['issueKey'])
        print(item['summary'])
        print(item['status']['name'])

    with open("ticket_s.csv", "w", encoding="shift_jis") as f:
        for item in json_obj:
            f.write(item['issueKey'] + "," + item['summary'] + "," + item['status']['name'] + "\n")

    with open("ticket.csv", "w", encoding="utf-8") as f:
        for item in json_obj:
            f.write(item['issueKey'] + "," + item['summary'] + "," + item['status']['name'] + "\n")

if __name__ == '__main__':
    #main()
    main2()
    