# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import urllib.request
from bs4 import BeautifulSoup

with open("test.html", "rb") as frp:
    buf = frp.read()
    soup = BeautifulSoup(buf, "html.parser")
    div =  soup.find('div', attrs={'class': 'thread'})
    #print(div)
    #print(type(div))
    with open("div.html", "w", encoding="utf-8") as fwp:
        fwp.write(str(div))
    