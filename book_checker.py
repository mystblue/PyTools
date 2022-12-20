# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup

set = {
    "07" : {"url_a": 'https://hon-hikidashi.jp/enjoy/150087/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/150088/'},
    "08" : {"url_a": 'https://hon-hikidashi.jp/enjoy/151491/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/151493/'},
    "09" : {"url_a": 'https://hon-hikidashi.jp/enjoy/152766/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/152767/'},
    "10" : {"url_a": 'https://hon-hikidashi.jp/enjoy/154368/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/154369/'},
    "11" : {"url_a": 'https://hon-hikidashi.jp/enjoy/156084/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/156085/'},
    "12" : {"url_a": 'https://hon-hikidashi.jp/enjoy/158107/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/158108/'},
    "01" : {"url_a": 'https://hon-hikidashi.jp/enjoy/159974/',
            "url_b": 'https://hon-hikidashi.jp/enjoy/159975/'}
}

url_a ='https://hon-hikidashi.jp/enjoy/156084/'
url_b = 'https://hon-hikidashi.jp/enjoy/156085/'

titles = ["女神のカフェテラス", "もののがたり", "ギルティサークル", "出会って5秒でバトル", "ぐらんぶる", "てんぷる", "バツハレ", "制裁学園", "EDENS", "イジらないで、長瀞さん", "恋愛志向生徒会", "トリアージ", "トリニティセブン", "カッコウの許嫁", "ダンダダン", "キングダム", "終末のハーレム", "はぐれアイドル", "魔都精兵のスレイブ", "あやかしトライアングル", "彼女、お借りします", "絶対聖域のチェリオン", "甘神さんちの縁結び", "俺の現実", "賭ケグルイ",  "性食鬼", "冒険王ビィト", "呪術廻戦", "さわらないで小手指くん", "化物語", "神呪のネクタール", "ダーウィンズゲーム", "チェンソーマン"]
authors = ["瀬尾公治", "冨樫義博", "あきばるいき", "オニグンソウ", "尾田栄一郎", "赤坂一夫", "真島ヒロ", "タスクオーナ", "佐原玄清", "堀越耕平", "春輝", "神田ゆう", "井荻寿一", "岬ゆきひろ"]

def download(url, filename):
    urlData = requests.get(url).content
    with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
      f.write(urlData)

def parse(filename):
    buf = ""
    ret = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    soup = BeautifulSoup(buf, "html.parser")
    body = soup.find(id="contents_body_main")
    table = body.find("table")
    rows = table.findAll("tr")
    for row in rows:
        for cell in row.findAll(['td', 'th']):
            ret = ret + cell.get_text().replace("\n", ",") + ","
        ret = ret + "\n"
    return ret

def main(month):
    buf = ""
    buf += parse(month + "a.html")
    buf += parse(month + "b.html")
    with open(month + ".csv", "w", encoding="utf-8") as f:
        f.write(buf)
    
    ret = ""
    skip = False

    splitted = buf.split("\n")
    print(len(splitted))
    for line in splitted:
        items = line.split(',')
        if len(items) > 4:
            for author in authors:
                if author in items[4]: # うまくa.csv が出力されない場合は、インデックスを確認する
                    ret = ret + line + "\n"
                    skip = True
            if not skip:
                for title in titles:
                    if title in items[3]: # うまくa.csv が出力されない場合は、インデックスを確認する
                        ret = ret + line + "\n"

        skip = False

    with open(month + "a.csv", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    month = "01"
    url_a = set[month]["url_a"]
    url_b = set[month]["url_b"]
    download(url_a, month + "a.html")
    download(url_b, month + "b.html")
    main(month)
