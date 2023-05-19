# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

# pip install requests
# pip install beautifulsoup4

from bs4 import BeautifulSoup

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")
    table = body.find_all("table")
    rows = table.findAll("tr")

    ret = ""
    for row in rows:
        for cell in row.findAll(['td', 'th']):
            ret = ret + cell.get_text().replace("\n", ",") + ","
        ret = ret + "\n"
    return ret

def main(month):
    buf = ""
    buf += parse("data.html")

if __name__ == '__main__':
    main()
