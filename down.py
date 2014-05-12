# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '0.0.1'

import urllib, urllib2

with open("test.html", "w") as frp:
    #f = urllib2.urlopen("https://book-checker.appspot.com/dl?url=http://comic.dawnfun.com/")
    #f = urllib2.urlopen("http://maohtorrent.blog101.fc2.com/blog-category-36.html")
    #http://blog.livedoor.jp/kinisoku/archives/3958138.html
    #http://book-checker.appspot.com/dl?url=
    f = urllib2.urlopen("http://book-checker.appspot.com/dl?url=http://blog.livedoor.jp/kinisoku/archives/3976144.html")
    frp.write(f.read())
