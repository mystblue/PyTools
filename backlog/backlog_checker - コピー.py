# -*- coding: utf-8 -*-
import csv
import json
import os
import requests
import pprint

milestone_id = "373344"
apikey = "FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf"

dir = "backlog_data"
issue_dir = "issue"
comment_dir = "comment"
attachment_dir = "attachment"
issue_list = "issue_list.json"

def get_issue_list():
    payload = {
        'apiKey': 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf',
        'projectId[]': ['111745'],
        'milestoneId[]': [milestone_id],
        'count': 100,
        'order': 'asc'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    issue_url = 'https://pcidss.backlog.jp/api/v2/issues?apiKey='
    issues = requests.get(issue_url + apikey, data = payload, headers = headers)
    
    print("該当する課題は" + str(len(issues.json())) + "件です。")
    with open(os.path.join(dir, issue_list), "w", encoding="utf-8") as f:
        f.write(json.dumps(issues.json()))

def get_issues():
    buf = ""
    with open(os.path.join(dir, issue_list), "r", encoding="utf-8") as f:
        buf = f.read()

    json_obj = json.loads(buf)
    
    issues = []
    for item in json_obj:
        issues.append(item['issueKey'])
    return issues

def get_issue_attachment():
    print("添付ファイル一覧を取得します。")
    issues = get_issues()
    for issue in issues:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        issue_url = 'https://pcidss.backlog.jp/api/v2/issues/' + issue + '/attachments?count=100&apiKey='
        issues = requests.get(issue_url + apikey, headers = headers)

        attachment_path = os.path.join(dir, attachment_dir)
        if not os.path.exists(attachment_path):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(attachment_path)

        with open(os.path.join(attachment_path, issue + ".json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(issues.json()))

def get_issue_comment():
    print("コメントを取得します。")
    issues = get_issues()
    for issue in issues:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        issue_url = 'https://pcidss.backlog.jp/api/v2/issues/' + issue + '/comments?count=100&apiKey='
        issues = requests.get(issue_url + apikey, headers = headers)

        comment_path = os.path.join(dir, comment_dir)
        if not os.path.exists(comment_path):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(comment_path)

        with open(os.path.join(comment_path, issue + ".json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(issues.json()))

def collect():
    print("バックログのデータ収集を開始します。")
    if not os.path.exists(dir):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(dir)
    # マイルストンに紐づけられた課題の一覧を取得
    get_issue_list()
    # コメントを取得
    get_issue_comment()
    # 添付ファイル一覧を取得
    get_issue_attachment()

def analysis():
    print("バックログの変更内容をチェックします。")
    buf = ""
    with open(os.path.join(dir, issue_list), "r", encoding="utf-8") as f:
        buf = f.read()

    json_obj = json.loads(buf)
    
    comment_path = os.path.join(dir, comment_dir)
    ret = ""
    
    ret = '"課題番号","課題概要","状態","git変更","添付ファイル"\n'
    
    for item in json_obj:
        ret = ret + "\"" + item['issueKey'] + "\",\"" + item['summary'] + "\",\"" + item['status']['name'] + "\""
        # コメントのチェック
        is_commit = False
        bufc = ""
        with open(os.path.join(comment_path, item['issueKey'] + ".json"), "r", encoding="utf-8") as f:
            bufc = f.read()
        comment_obj = json.loads(bufc)
        for comment in comment_obj:
            logs = comment['changeLog']
            for log in logs:
                if log['field'] == 'commit':
                    is_commit = True
        
        if is_commit:
            ret = ret + ",\"〇\""
        else:
            ret = ret + ",\"×\""
        
        # 添付ファイルのチェック
        attachment_path = os.path.join(dir, attachment_dir)
        bufa = ""
        with open(os.path.join(attachment_path, item['issueKey'] + ".json"), "r", encoding="utf-8") as f:
            bufa = f.read()
        attachment_obj = json.loads(bufa)
        
        ret = ret + ",\""
        for attachment in attachment_obj:
            ret = ret + attachment['name'] + "\n"
        ret = ret + "\""
        
        ret = ret + "\n"

    with open("ticket_s.csv", "w", encoding="shift_jis") as f:
        f.write(ret)

def main():
    collect()
    analysis()

if __name__ == '__main__':
    main()
    