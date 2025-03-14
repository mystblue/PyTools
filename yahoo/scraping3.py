# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4
# pip install lxml

from bs4 import BeautifulSoup
import os
import requests

def parse(url):
    buf = ""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    ret = ""

    h1tag  = soup.select("article header h1")
    print(type(h1tag))
    print(h1tag[0].text)
    ret += h1tag[0].text + "\n\n"

    ptag  = soup.select("article div div  p")
    print(type(ptag))
    print(len(ptag))
    print(ptag[0].text)
    print(ptag[1].text)
    print(ptag[2].text)
    for item in ptag:
        ret += item.text

    return ret

def main():
    ret = parse("https://news.yahoo.co.jp/articles/55991c1ca75baf8afef517e44241e0a75512a8a8?page=2")
    
    with open("test5.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main()
