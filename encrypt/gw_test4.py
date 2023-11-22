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
    data = '''GT2MP2bQBC+EQciyqd96GJAop4SIUE1C/KWL7ZBPJNfNCgFmugHz1XSSG38q8pW6pSl6RQDoJ8qi
EcutxejJKPUJdP8gvuK9wNjCyWgYObMICeFPex0c2LrSzli8ZhTVdM43gGQjKbimHNMF0XvV/AcQ
7jlV3JvU0tsOcCGBfzuG9jlQthDeTM3he+gZIQrzLGS6lQf6Ssdw9H7U+wmgaRzMUkGjtKblACXe
kGwkPFchQzJy3/OeovMsXdKv+3Cr0OG6kb3wjXrh+Lv08emj1SbE0yej+dbSLhgUx/kK6TE='''
    text = base64.b64decode(data)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    #mes = Padding.unpad(mes, 32)
    print(mes)
    res = unquote(mes.decode('utf-8'))
    #res = Padding.unpad(res, AES.block_size, 'pkcs7')
    print(res)
    dic = urllib.parse.parse_qs(res)
    keys = dic.keys()
    for key in keys:
        print(key + ": " + dic[key][0])
    