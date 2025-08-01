# -*- coding: utf-8 -*-

"""
"""

import bs4
from bs4 import BeautifulSoup
import re
import requests

def cut(filename, dst):
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()

    soup = BeautifulSoup(buf, "html.parser")
    main = soup.find(id="main-contents")

    scripts = main.find_all('script')
    for script in scripts:
        script.decompose()

    scripts = main.find_all('noscript')
    for script in scripts:
        script.decompose()

    scripts = main.find_all('style')
    for script in scripts:
        script.decompose()

    target = None
    h2s = main.find_all('h2')
    for h2 in h2s:
        if h2.text == '関連記事':
            if not target:
                target = h2
            else:
                print("error")

    del_list = [target]
    if target:
        for tag in target.next_siblings:
            if type(tag) == bs4.element.Tag:
                del_list.append(tag)
    
    for item in del_list:
        item.decompose()

    div = main.find('div', class_="copyWrap")
    if div:
        div.decompose()

    ret = str(main)

    with open(dst ,mode='w', encoding="utf-8") as f:
        f.write(ret)

def download(url, filename):
    urlData = requests.get(url).content
    with open(filename ,mode='wb') as f:
        f.write(urlData)

if __name__ == '__main__':
    #download("https://altema.jp/houkaistarrail/kaitaku", "kaitaku.html")
    download("https://yurasama.sakura.ne.jp/game/comp/kaguya_jd.html", "kaguya_jd")
    #cut("kaitaku.html", "kaitaku.txt")
