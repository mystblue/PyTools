# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

from bs4 import BeautifulSoup
import os

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")

    ret = ""

    main_tag = soup.find_all("main")
    #print(type(main_tag))
    #print(len(main_tag))
    
    result = main_tag[0].find_all("img")
    #print(len(result))
    #print(result)
    
    for a_tag in result:
        print(a_tag["src"])
        ret += a_tag["src"] + "\n"
    
    return ret

def main():
    buf = parse("karuizawa.html")
    
    with open("list.txt", "w", encoding="utf-8") as f:
        f.write(buf)

if __name__ == '__main__':
    main()
