# -*- coding: utf-8 -*-
import csv
import json
import requests
import pprint

def main():
    apikey = "xxx"
    
    url = "https://pcidss.backlog.jp/api/v2/projects/111745/versions?apiKey=" + apikey
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    issues = requests.get(url, headers = headers)

    json_obj = issues.json()
    for item in json_obj:
        print(item["name"] + " : " + str(item["id"]))

if __name__ == '__main__':
    main()
