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

request = 'PC0823B910118,20240919185120'



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
    
    enc = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    data = Padding.pad(request.encode('utf-8'), AES.block_size, 'pkcs7')
    ret = enc.encrypt(data)
    print(base64.b64encode(ret))
    
    # POST with header
    #url = 'https://paytg-dev-nlb-c3c06871f9f770a9.elb.ap-northeast-1.amazonaws.com:10443/css/font/ficon.woff?206623=+AND+1%3D1+--+'
    url = 'https://paytg-dev-nlb-c3c06871f9f770a9.elb.ap-northeast-1.amazonaws.com:10443/css/font/ficon.woff?206623=+OR+1%3D1+--+'
    r = requests.get(url, verify=False)
    print(r.status_code)
    print(r.text)
    print(r.headers)
    text = base64.b64decode(r.text)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    mes = Padding.unpad(mes, AES.block_size, 'pkcs7')
    print(mes.decode("utf-8"))
