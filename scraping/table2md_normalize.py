# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

import os
import re

def parse(filename):
    buf = ""
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    ret = re.sub('<td [^>]*>\n[ ]+', '<td>', buf)
    ret = re.sub('\n[ ]+</td>', '</td>', ret)
    ret = re.sub('<br>\n[ ]+', '<br>', ret)

    return ret

def main():
    buf = parse("table.html")

    with open("table.html", "w", encoding="utf-8") as f:
        buf = f.write(buf)

if __name__ == '__main__':
    main()
