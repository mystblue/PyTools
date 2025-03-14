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

    divtags  = soup.select("div.NA_article_body")
    #print(divtag)
    #print(len(divtags))
    if len(divtags) == 1:
        divtag = divtags[0]
        h2tags = divtag.select("h2")
        for h2tag in h2tags:
            #print(h2tag["class"])
            #print(h2tag.get("class"))
            #print(h2tag.text)
            # id 属性があり「NA_article_main_」で始めれば
            if h2tag.get("id") and h2tag.get("id").startswith("NA_article_main_"):
                #print(h2tag.text)
                #print(h2tag.next_sibling)
                ret += h2tag.text + "\n"
                #print(h2tag.next_sibling.contents)
                for item in h2tag.next_sibling.contents:
                    if item.name == 'a':
                        print('a')
                        ret += item.text
                    elif item.name == 'br':
                        print('改行')
                        ret += "\n"
                    elif item.name == 'wbr':
                        print('wbr')
                    else:
                        ret += item
                ret += "\n\n"
    
    return ret

def main():
    ret = parse("data.html")
    
    with open("test2.txt", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main()
