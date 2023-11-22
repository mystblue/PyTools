# -*- coding: utf-8 -*-

import base64

import requests

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib.parse
from urllib.parse import unquote

iv = "cc7b9247ed6f8f7c41e9dcce0d340ef4"
sn = '000118183306329'

request = 'requestDate=20230224183901&sn=000118183306329&cardNumber=4111111111111111&cardExpire=1225&securityCode=8888&orderId=8888aaaaaaaaaagwewataa2&ttyId=00000027000112023091900032&category=4&transactionDate=20230224183901'



def get_iv(str):
    # hex2bin 相当
    return bytes.fromhex(str)

def get_key(sn):
    seed = 'a949a6df9433d8cab20eb6f397e09540'
    seed_use = seed[0:17]
    key_org = sn + seed_use
    key_orgs = key_org[0:32]
    return bytes.fromhex(key_orgs)

if __name__ == '__main__':
    print(base64.b64encode(get_iv(iv)))
    print(base64.b64encode(get_key(sn)))
    print(type(base64.b64encode(get_key(sn))))
    
    reflesh_length = AES.block_size - len(request) % AES.block_size
    #request += chr(16) * reflesh_length
    
    enc = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    data = Padding.pad(request.encode('utf-8'), AES.block_size, 'pkcs7')
    ret = enc.encrypt(data)
    print(base64.b64encode(ret))
    
    
    
    headers = {'IV': iv, 'SN':sn, 'Sver': '1000'}
    # POST with header
    r = requests.post('https://10.200.91.141', 
        data=base64.b64encode(ret),
        headers=headers, verify=False)
    print(r.status_code)
    print(r.text)
    text = base64.b64decode(r.text)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    print(mes)
    mes = Padding.unpad(mes, AES.block_size, 'pkcs7')
    print(mes.decode("utf-8"))
    print(urllib.parse.parse_qs(mes.decode("utf-8")))
    