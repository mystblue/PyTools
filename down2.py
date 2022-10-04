# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import urllib.request#, urllib2

with open("testb.html", "wb") as frp:
    #http://book-checker.appspot.com/dl?url=
    #f = urllib2.urlopen("http://book-checker.appspot.com/dl?url=https://mevius.5ch.net/test/read.cgi/gamerobo/1635337031/")
    #f = urllib.request.urlopen(url = "https://ds-can.com/srw30/system/birthday.html")
    opener = urllib.request.build_opener()
    opener.addheaders =  [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30')]
    f = opener.open("https://ds-can.com/srw30/system/birthday.html")
    
    #headers = { "User-Agent" :  "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }
    #f = urllib.request.add_header('User-Agent', 'Mozilla/5.0').urlopen("https://mevius.5ch.net/test/read.cgi/gamerobo/1635393192/")
    #frp.write(f.read())
    frp.write(f.read())