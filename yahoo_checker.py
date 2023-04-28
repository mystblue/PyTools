# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

import datetime
import requests
from bs4 import BeautifulSoup

def download(url, filename):
    urlData = requests.get(url).content
    with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
        f.write(urlData)

def parse(filename):
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    soup = BeautifulSoup(buf, "html.parser")
    topics = soup.find(id="tabpanelTopics1")
    a_tags = topics.findAll("a")
    for a_tag in a_tags:
        print(type(a_tag))
        print(a_tag)
        print()

def main(file_name):
    parse(file_name)

def yahoo_download():
    now = datetime.datetime.now()
    file_name = "yahoo_" + now.strftime('%Y%m%d_%H%M%S') + ".html"
    download("https://www.yahoo.co.jp", file_name)
    return file_name

if __name__ == '__main__':
    #file_name = yahoo_download()
    main("yahoo_20230426_133442.html")
