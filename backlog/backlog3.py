# -*- coding: utf-8 -*-
import csv
import requests
import pprint

def main():

    payload = {
        'apiKey': 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf',   # xxxxx は API キーを設定
        'projectId[]': ['111745'],
        'milestoneId[]': ['373344']
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    issues = requests.get('https://pcidss.backlog.jp/api/v2/issues/count?apiKey=' + 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf', data = payload, headers = headers) # xxxxx は環境にあわせて設定

    #pprint.pprint(issues.json())
    print(issues)
    pprint.pprint(issues.json())

if __name__ == '__main__':
    main()