# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import urllib.request

with open("test.html", "wb") as frp:
    opener = urllib.request.build_opener()
    opener.addheaders =  [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30')]
    f = opener.open("https://mevius.5ch.net/test/read.cgi/gamerobo/1635393192/")
    frp.write(f.read())