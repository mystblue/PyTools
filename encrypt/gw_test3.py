# -*- coding: utf-8 -*-

import base64

import requests

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib.parse
from urllib.parse import unquote

iv = "B4A64A7CDDE702C48BFBDA0AAABBE868"
sn = '000118180200194'

def get_iv(str):
    # hex2bin 相当
    return bytes.fromhex(str)

def get_key(sn):
    seed = 'a949a6df9433d8cab20eb6f397e09540'
    #seed = '26ec152e29b34d5f801c9a96bdd43a66'
    seed_use = seed[0:17]
    key_org = sn + seed_use
    key_orgs = key_org[0:32]
    return bytes.fromhex(key_orgs)

if __name__ == '__main__':
    data = 'tnDQzqjYsXeCqUd3URcoksOyS8E7z6u6inU2R5hJhPveWbe+xzL4zk8v68b06KktKLOtnoK/xd4+zz5WOqed1WxkUxFQxq6H+wEBoy6ECGYcf1TaW3IQI3u9iW8QqWiD7PofXGPMOnlvPKlTM4Q9ZWnYbR9XaDUceghGKO1DpPGu4GyPNzxxquGApdb2wH8K'
    #data = ''
    #data = ''
    #data  = 'bHKKULCPHmXO6BsaPVk3tw=='
    """


1PVVB5Q4HRxCESeaAAO/eNItGHWHNEO6jqYm5q+s+BwUzMgavRR3xE2N0RkhJUQm
XrxwDYJ5QlhW3ZniSaG+/q2OLNNwvKhTbf32bCrvwPOr78ooShDm9Eu6IYwvxFoM

"""
    text = base64.b64decode(data)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    #print(mes)
    res = unquote(mes.decode('utf-8'))
    #print(res)
    dic = urllib.parse.parse_qs(res)
    keys = dic.keys()
    for key in keys:
        print(key + ": " + dic[key][0])
    