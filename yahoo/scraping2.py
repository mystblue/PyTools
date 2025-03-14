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

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")

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
    ret = parse("data.html")
    
    with open("test2.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main()
