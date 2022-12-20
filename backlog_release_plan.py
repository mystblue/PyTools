# -*- coding: utf-8 -*-
import csv
import json
import os
import requests
import pprint

milestone_id = "373344"
apikey = "xxx"

dir = "backlog_data"
issue_dir = "issue"
comment_dir = "comment"
attachment_dir = "attachment"
issue_list = "issue_list.json"

def analysis():
    print("バックログの変更内容をチェックします。")
    buf = ""
    with open(os.path.join(dir, issue_list), "r", encoding="utf-8") as f:
        buf = f.read()

    json_obj = json.loads(buf)
    
    comment_path = os.path.join(dir, comment_dir)
    ret = ""
    
    ret = ret + "|NO|チケット|概要|DB|GW|TMS|TMSWEB|HSM|h\n"

    counter = 1

    for item in json_obj:
        ret = ret + "|" + str(counter) + "|" +  item['issueKey'] + "|" + item['summary'] + "|-|-|-|-|-|"
        
        ret = ret + "\n"
        counter += 1

    with open("release_plan.txt", "w", encoding="utf-8") as f:
        f.write(ret)



    ret = "|NO|チケット|概要|DB更新|Git更新|管理画面設定|ミドルウェア設定変更|ミドルウェアVUP|h\n"

    counter = 1

    for item in json_obj:
        ret = ret + "|" + str(counter) + "|" +  item['issueKey'] + "|" + item['summary'] + "|-|-|-|-|-|"
        
        ret = ret + "\n"
        counter += 1

    with open("release_plan2.txt", "w", encoding="utf-8") as f:
        f.write(ret)

def main():
    analysis()

if __name__ == '__main__':
    main()
    