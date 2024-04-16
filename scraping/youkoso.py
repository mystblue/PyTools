# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

import bs4
from bs4 import BeautifulSoup
import os

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")

    ret = ""

    divs = soup.find_all("div")
    print(len(divs))
    for h3 in divs:
        ps = h3.contents
        for p in ps:
            if p.name == "p":
                items = p.contents
                #for item in items:
                for i, item in enumerate(items):
                    if type(item) is bs4.element.Tag:
                        #print("タグです")
                        if item.name == 'ruby':
                            #print("ルビです")
                            rbs = item.contents
                            rt = ''
                            rb = ''
                            for r in rbs:
                                if type(r) is bs4.element.Tag:
                                    if r.name == 'rb':
                                        rb = r.text
                                    if r.name == 'rt':
                                        rt = r.text
                            if rt and rt:
                                ret += "[" + rt + "](-" + rb + ")"
                        elif item.name == 'br':
                            #ret += "\n"
                            pass
                        else:
                            print("未知のタグです。" + item.name)
                    else:
                        if i == 0 and item.startswith('　'):
                            ret += item.text[1:]
                        else:
                            ret += item.text
                ret += "\n"
    return ret

def main():
    buf = parse("youkoso.html")

    #buf = "var contents = `" + buf + "`;"

    with open("youkoso.js", "w", encoding="utf-8") as f:
        buf = f.write(buf)

if __name__ == '__main__':
    main()
