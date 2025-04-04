# -*- coding: utf-8 -*-

"""
ファイルをダウンロードするスクリプト
"""

__author__  = 'mystblue'
__version__ = '1.0.0'

import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def main():
    url='https://i.pximg.net/img-master/img/2025/03/23/03/30/37/128504567_p0_master1200.jpg'
    filename='128504567_p0_master1200.jpg'
    
    urlData = requests.get(url, headers=headers).content
    
    with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
        f.write(urlData)

if __name__ == '__main__':
    main()
