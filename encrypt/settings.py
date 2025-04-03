#url = 'https://10.200.91.141'
#url = 'https://dev-gw-v2-tmp.paytg.jp'
#url = 'https://d-i2m75i237h.execute-api.ap-northeast-1.amazonaws.com'
#url = 'https://dev-gw-v2.paytg.jp?username=admin&password=password%27%20OR%20%271%27=%271'
#url = 'https://dev-gw-v2.paytg.jp/robots.txt'
url = 'https://dev-gw-v2.paytg.jp'
#url = 'https://stg-gw-v2.paytg.jp'
#url = 'https://stg-trialgw-v2.paytg.jp'
#url = 'https://7zgobn6rmh.execute-api.ap-northeast-1.amazonaws.com/v1'?status=1%0d%0aSet-Cookie:%20sessionid%3d12345678
#url = 'https://paytg-dev-apigw-gw-test'
#url = 'https://d-xegj6618e6.execute-api.ap-northeast-1.amazonaws.com'
#url = 'https://localhost'

seed = 'a949a6df9433d8cab20eb6f397e09540'

cert = './cert/D19CF1C348EAB5AA.pem'
#cert = './cert/D9DAA9555C27F998.pem' # ステージング環境
#cert = './cert/D9DAA9555C27F936.pem'

psp_list = ['sony']
"""
psp_list = [
    'dgft',
    'sony',
    'paygent',
    'gmo-pg',
    'smbc-fs',
    'yamato',
    'zeus',
    'smbc-gmo',
    'gmo-mb',
    'nicos-pg',
    'ncoms',
    'rakuten',
    'pay-jp',
    'sbps',
]
"""
terminal = {
    'paygent' :  {
                     'sn'    : '338534947935133',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000400001'
                 },
    'ncoms' :    {
                     'sn'    : '711359556720335',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001200001'
                 },
    'dgft' :     {
                     'sn'    : '239185119488177',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000100001'
                 },
    'gmo-pg' :   {
                     'sn'    : '308244202700682',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000500001'
                 },
    'pay-jp' :   {
                     'sn'    : '334714378614310',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000002700001'
                 },
    'sony' :     {
                     'sn'    : '360315259670395',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000200001'
                 },
    'rakuten' :  {
                     'sn'    : '334714378614309',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000002000003'
                 },
    'sbps' :     {
                     'sn'    : '440808393041355',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000003200005'
                 },
    'smbc-fs' :  {
                     'sn'    : '045538703227172',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000600001'
                 },
    'smbc-gmo' : {
                     'sn'    : '875465933803912',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000900001'
                 },
    'yamato' :   {
                     'sn'    : '358014990049381',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000700001'
                 },
    'zeus' :   {
                     'sn'    : '596992594557941',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000800001'
                 },
    'gmo-mb' :   {
                     'sn'    : '165877551409492',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001000001'
                 },
    'gmo-mb-m' :   {
                     'sn'    : '751347591905118',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001300001'
                 },
    'nicos-pg' :   {
                     'sn'    : '334714378614308',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001400004'
                 },
}

