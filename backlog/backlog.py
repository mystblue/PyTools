import csv
import pprint
import sys
import requests
def main():
    """Backlog に登録されている課題を以下の条件で取得し CSV 形式で出力する
    - 対象プロジェクト: 「あいうえおプロジェクト」「かきくけこプロジェクト」
    - ステータス: 「未対応」「処理中」
    - 担当者: 「佐藤宏行」
    - 並び順: 期限日の降順
    """
    target_projects = {
        PTG_DEV: 'PTG_DEV',        # xxxxx の部分には、上で取得したプロジェクトIDを設定して下さい
        PTG_WIN: 'PTG_WIN',        # （同上）
    }
    target_statuses = [
        1, # 未対応
        2, # 処理中
    ]
    payload = {
        'apiKey': 'FIVdvY4Chw9MbP2wph6Mybyb6aTf6LrgvlR99PugXy8OKbZYHPRQb4Qxnn2keSOf',
        'projectId[]': [list(target_projects.keys())],  # 対象プロジェクトを指定
        'statusId[]': [target_statuses],                # ステータス「未対応」「処理中」追加
        'assigneeId[]': ['k-kayama-bog'],                        # 担当者に私（佐藤宏行）を追加
        'sort': 'dueDate',                              # 並び替えの指定: "期限日"
        'order': 'desc',                                #               "降順"
    }
    issues = requests.get('https://ap3.backlog.com/api/v2/issues', payload)
    results = []
    for issue in issues.json():
        result = {
            'プロジェクトID': issue['projectId'],
            'プロジェクト名': target_projects[issue['projectId']],
            '件名': issue['summary'],
            'ステータス': issue['status']['name'],
            '期限日': issue['dueDate'] if issue['dueDate'] else '（指定なし）',
        }
        results.append(result)
    sys.stdout.close = lambda: None
    with (sys.stdout) as f:
        writer = csv.DictWriter(f,
                                quotechar='"',
                                quoting=csv.QUOTE_ALL,
                                fieldnames=list(results[0].keys()))
        writer.writeheader()
        
        for i, r in enumerate(results, start=1):
            writer.writerow(r)
if __name__ == '__main__':
    main()