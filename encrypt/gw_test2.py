# -*- coding: utf-8 -*-

import base64

import requests

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib.parse
from urllib.parse import unquote

iv = "cc7b9247ed6f8f7c41e9dcce0d340ef4"
sn = '916501470337666'

form_data = {
    'requestDate' : '20230224183901',
    'sn' : sn,
    'cardNumber' : "4111111111111111",
    'cardExpire' : "1225",
    "securityCode" : "8888",
    "orderId" : "8888aaaaaaaaaagwewataa2",
    'ttyId' : '00000027000012023091900032',
    'category' : '1',
    'transactionDate' : '20230224183901'
}

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
    
    request = urllib.parse.urlencode(form_data)
    
    enc = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    data = Padding.pad(request.encode('utf-8'), AES.block_size, 'pkcs7')
    ret = enc.encrypt(data)
    
    headers = {'IV': iv, 'SN':sn, 'Sver': '1000'}
    # POST with header
    r = requests.post('https://10.200.91.8', 
        data=base64.b64encode(ret),
        headers=headers,
        verify=False)
    print("statusCode = " + str(r.status_code))
    #print(r.text)
    text = base64.b64decode(r.text)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    #print(mes)
    res = unquote(mes.decode('utf-8'))
    #print(res)
    dic = urllib.parse.parse_qs(res)
    keys = dic.keys()
    for key in keys:
        print(key + ": " + dic[key][0])
    