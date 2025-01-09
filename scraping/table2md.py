# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

from bs4 import BeautifulSoup
import os

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")

    ret = ""

    table = soup.find("table")
    rows = table.findAll("tr")
    for trs in rows:
        for cell in trs:
            if cell.name == "th":
                ret = ret + "|_." + cell.text
            if cell.name == "td":
                if len(cell.find_all("p")) > 0:
                    #print(cell.find_all("p")[0].text)
                    ret = ret + "|"
                    for p in cell.find_all("p"):
                        ret = ret + p.text.strip() + "<br>"
                    ret = ret[:-4]
                else:
                    ret = ret + "|" + cell.text
        ret += "|\n"

    return ret

def main():
    buf = parse("table.html")

    with open("table.md", "w", encoding="utf-8") as f:
        buf = f.write(buf)

if __name__ == '__main__':
    main()
