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
from lxml import html
from lxml import etree

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")
    lxml_data = html.fromstring(str(soup))

    ret = ""

    h1tag  = lxml_data.xpath("//article/header/h1")
    ret += h1tag[0].text + "\n\n"

    ptag  = lxml_data.xpath("//article/div/div/p")
    ret += etree.tostring(ptag[0], encoding='utf-8')
    """
    #ret += ptag[0].text
    print(type(ptag))
    print(len(ptag))
    for item in ptag:
        print(type(item))
        print(item.text)
        print(item.tail)
        ret += item.text
        for ob in item:
            print(type(ob))
            print(ob.text)
            print(ob.tail)
            ret += ob.text
            ret += ob.tail
    """
    return ret

def main():
    ret = parse("data.html")
    
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main()
