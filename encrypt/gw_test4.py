# -*- coding: utf-8 -*-

import base64

import requests

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib.parse
from urllib.parse import unquote

iv = "7BB15B1D25C7C6758B1C9A5A2A10AFBF"
sn = '112104906700517'

def get_iv(str):
    # hex2bin 相当
    return bytes.fromhex(str)

def get_key(sn):
    #seed = 'BEC4423F86E5EE5AF61934D924721FC4'
    #seed = '2eb3f47dd0cde34f2ca7ff341a5438d7'
    seed = 'c04cf22df5bd069df4366ba921cce596'
    seed_use = seed[0:17]
    key_org = sn + seed_use
    key_orgs = key_org[0:32]
    return bytes.fromhex(key_orgs)

if __name__ == '__main__':
    data = '5UrOrNd++1hB7LPAfIJZ1NNBcA+VsJSbi7NLN71fslE='
    text = base64.b64decode(data)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    print(mes)
    res = unquote(mes.decode('utf-8'))
    print(res)
    dic = urllib.parse.parse_qs(res)
    keys = dic.keys()
    for key in keys:
        print(key + ": " + dic[key][0])
    