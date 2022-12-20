# -*- coding: utf-8 -*-
import csv
import json
import requests
import pprint

def main():
    apikey = "FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf"
    
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


"""
>python backlog_milestone.py
2022/11月リリース : 373344
2022/10/05リリース : 370242
2022/9/14 GW リリース : 367378
2022/7/27 リリース : 364298
P2PRO V1.0.03→1.0.04 : 361935
2022/7/14 Pay TG リリース : 361934
2022/03/10リリース : 349284
2022/01/27 リリース : 343053
P2PRO V1.0.01 : 340163
2021/11/10 リリース : 336114
2021/10/07 リリース : 324328
Smart TG 営業契約関連 : 318835
2021/06/03 リリース : 317407
2021/04/22 リリース : 311603
2021/02/25 リリース : 300942
2021/02/04 リリース : 300022
2020/12/03 リリース : 295629
Smart TG開発 : 295548
2020/10/28 リリース : 294517
2020/10/22 リリース : 293651
2020/9/30 リリース : 280711
2020/6/17リリース : 277459
マルチPSP対応 : 264946
2020/2/26 リリース : 264082
2020/2/6 リリース : 261613
2019年11月リリース : 253487
NTTコムオンライン追加接続 : 238984
QTnet BIN判定表示機能開発 : 224635
三菱UFJニコス 追加接続 : 222012
"""
