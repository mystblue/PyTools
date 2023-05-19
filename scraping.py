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

    h2s = soup.find_all("h2")
    print(len(h2s))
    for h2 in h2s:
        ret = ret + "## " + h2.text + "\n\n"
        div = h2.next_sibling.next_sibling
        for child in div.children:
            if child.name == "table":
                rows = child.findAll("tr")
                for trs in rows:
                    for cell in trs:
                        if cell.name == "th":
                            if 'rowspan' in cell.attrs:
                                ret = ret + "|/2_." + cell.text
                            elif 'colspan' in cell.attrs:
                                ret = ret + "|\\\\4_=." + cell.text
                            else:
                                ret = ret + "|_." + cell.text
                        if cell.name == "td":
                            ret = ret + "|" + cell.text
                    ret = ret + "|\n"

    return ret

def main():
    buf = parse("data.html")

    buf = "var contents = `" + buf + "`;"

    with open("table.txt", "w", encoding="utf-8") as f:
        buf = f.write(buf)

if __name__ == '__main__':
    main()
