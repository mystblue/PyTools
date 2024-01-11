#url = 'https://10.200.91.141'
url = 'https://dev-gw-v2.paytg.jp'
#url = 'https://localhost'

seed = 'a949a6df9433d8cab20eb6f397e09540'

cert = './cert/D19CF1C348EAB53B.pem'

psp_list = ['pay-jp']
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
                     'sn'    : '883587303990566',
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
                     'sn'    : '916501470337654',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000003600001'
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
                     'sn'    : '736975652462638',
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
    'nicos-pg' :   {
                     'sn'    : '334714378614307',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001400003'
                 },
}

