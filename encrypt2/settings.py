url = 'https://dev-gw-v2.paytg.jp' # 開発用 GW

seed = 'a949a6df9433d8cab20eb6f397e09540'

cert = './cert/D19CF1C348EAB5AA.pem'

psp_list = ['sbps']
"""
psp_list = [
    'dgft',
    'sony',
    'paygent',
    'gmo-pg',
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
    'dgft' :  {
                     'sn'    : 'PC0823B9A2345', 
                     'CHGSN' : '50433038323342394132333435', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000100085'
                 },
    'sony' :  {
                     'sn'    : 'PC0823B91B345', 
                     'CHGSN' : '50433038323342393142333435', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000200022'
                 },
    'paygent' :  {
                     'sn'    : 'PC0823B912C45', 
                     'CHGSN' : '50433038323342393132433435', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000300013'
                 },
    'gmo-pg' :  {
                     'sn'    : 'PC0823B9123D5', 
                     'CHGSN' : '50433038323342393132334435', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000500009'
                 },
    'yamato' :  {
                     'sn'    : 'PC0823B91234E', 
                     'CHGSN' : '50433038323342393132333445', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000700003'
                 },
    'zeus' :  {
                     'sn'    : 'PC0823B9ABCDE', 
                     'CHGSN' : '50433038323342394142434445', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000800002'
                 },
    'smbc-gmo' :  {
                     'sn'    : 'PC0823B9ABC45', 
                     'CHGSN' : '50433038323342394142433435', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000000900008'
                 },
    'gmo-mb' :  {
                     'sn'    : 'PC0823B9123FG ', 
                     'CHGSN' : '50433038323342393132334647', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000001000004'
                 },
    'ncoms' :  {
                     'sn'    : 'PC0823B9HIJKL ', 
                     'CHGSN' : '504330383233423948494A4B4C', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000001200009'
                 },
    'rakuten' :  {
                     'sn'    : 'PC0823B9MNOPQ', 
                     'CHGSN' : '50433038323342394D4E4F5051', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000002100003'
                 },
    'pay-jp' :  {
                     'sn'    : 'PC0823B9QRSTU', 
                     'CHGSN' : '50433038323342395152535455', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000002700003'
                 },
    'sbps' :  {
                     'sn'    : 'PC0823B9VWXYZ', 
                     'CHGSN' : '5043303832334239565758595A', 
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '3000',
                     'ttyid' : '0000003300005'
                 }
}

