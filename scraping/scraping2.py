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

    h3s = soup.find_all("h3")
    print(len(h3s))
    for h3 in h3s:
        ret = ret + "## " + h3.text + "\n\n"
        div = h3.next_sibling.next_sibling
        ret += div.text + "\n"
        table = div.next_sibling.next_sibling
        if table.name == "table":
            rows = table.findAll("tr")
            for trs in rows:
                for cell in trs:
                    if cell.name == "td":
                        if len(cell.find_all("p")) > 0:
                            #print(cell.find_all("p")[0].text)
                            ret = ret + "|"
                            for p in cell.find_all("p"):
                                ret = ret + p.text.strip() + "<br>"
                            ret = ret[:-4]
                        else:
                            ret = ret + "|_." + cell.text
                ret += "|\n"

    return ret

def main():
    buf = parse("data2.html")

    buf = "var contents = `" + buf + "`;"

    with open("map.js", "w", encoding="utf-8") as f:
        buf = f.write(buf)

if __name__ == '__main__':
    main()
