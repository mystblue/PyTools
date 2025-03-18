# -*- coding: utf-8 -*-

import base64

import requests

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib.parse
from urllib.parse import unquote

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

iv = "6FC6F658DBE121BF8E481D616D0A7430"
sn = 'PC0823B910118'
chgsn = '082306605710118'

request = '000120240726091,20230924114100'



def get_iv(str):
    # hex2bin 相当
    return bytes.fromhex(str)

def get_key(sn):
    seed = '5f3d73cf95b49e7f95763193c833432b'
    seed_use = seed[0:17]
    key_org = chgsn + seed_use
    key_orgs = key_org[0:32]
    return bytes.fromhex(key_orgs)

if __name__ == '__main__':
    reflesh_length = AES.block_size - len(request) % AES.block_size
    
    with open("log.zip", "rb") as f:
        buf = f.read()
    
    enc = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    #data = Padding.pad(request.encode('utf-8'), AES.block_size, 'pkcs7')
    data = Padding.pad(buf, AES.block_size, 'pkcs7')
    ret = enc.encrypt(data)
    print(base64.b64encode(ret))
