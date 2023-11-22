# -*- coding: utf-8 -*-

import base64
import datetime
import json
import requests
import settings
import urllib.parse
from urllib.parse import unquote

import Crypto.Cipher.AES as AES
from Crypto.Util import Padding

import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def get_iv(str):
    # hex2bin 相当
    return bytes.fromhex(str)

def get_key(sn):
    seed = 'a949a6df9433d8cab20eb6f397e09540'
    seed_use = seed[0:17]
    key_org = sn + seed_use
    key_orgs = key_org[0:32]
    return bytes.fromhex(key_orgs)

def create_request_param(sn, iv, request_param):
    request = urllib.parse.urlencode(request_param)

    print('・request = ' + request)
    enc = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    data = Padding.pad(request.encode('utf-8'), AES.block_size, 'pkcs7')
    ret = enc.encrypt(data)
    encrypt_data = base64.b64encode(ret)
    return encrypt_data

def http_connect(sn, iv, request):
    headers = {'IV': iv, 'SN':sn, 'Sver': '1000'}
    # POST with header
    response = requests.post(settings.url, 
                   data=request,
                   headers=headers,
                   verify=False,
                   cert=settings.cert)
    return response

def print_response(sn, iv, respose):
    text = base64.b64decode(respose.text)
    dec = AES.new(key=get_key(sn), mode=AES.MODE_CBC, iv=get_iv(iv))
    mes = dec.decrypt(text)
    #print(mes)
    mes = Padding.unpad(mes, AES.block_size, 'pkcs7')
    #print(mes.decode("utf-8"))
    print(urllib.parse.parse_qs(mes.decode("utf-8")))

if __name__ == '__main__':
    print("■GW URL = " + settings.url + "\n")
    for psp in settings.psp_list:
        print("■PSP = " + psp)
        
        # 端末情報取得
        term = settings.terminal[psp]
        
        # パラメータ json 読み込み
        request_param_list = []
        with open('json\\' + psp + '.json', 'r', encoding="utf-8") as fp:
            request_param_list = json.load(fp)
        
        now = datetime.datetime.now()
        datetime_str = now.strftime('%Y%m%d%H%M%S')
        date_str = now.strftime('%Y%m%d')
        
        # PSP ごとの処理
        for request_param in request_param_list:
            request_param['requestDate'] = datetime_str
            request_param['transactionDate'] = date_str
            request_param['ttyId'] = term['ttyid'] + datetime_str[:-1]
            request_param['sn'] = term['sn']
            
            request = create_request_param(term['sn'], term['iv'], request_param)
                        
            response = http_connect(term['sn'], term['iv'], request)
            print("\nstatus code = " + str(response.status_code))
            print("\n・response = ")
            print(response.text)
            
            print_response(term['sn'], term['iv'], response)
            