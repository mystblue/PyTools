# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

from bs4 import BeautifulSoup
from lxml import html
import os

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")

    ret = ""

    h2s = soup.find_all("h2")
    print(len(h2s))
    
    dom = html.fromstring(str(soup))
    
    # XPathで要素を取得
    elements = dom.xpath("//div/section/h2")
    
    return elements

def main():
    buf = parse("release.html")
    for el in buf:
        print(el.text)

if __name__ == '__main__':
    main()
