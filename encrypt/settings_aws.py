#url = 'https://10.200.91.141'
url = 'https://dev-gw-v2.paytg.jp'

seed = 'a949a6df9433d8cab20eb6f397e09540'

cert = './cert/D19CF1C348EAB53B.pem'

#psp_list = ['sbps']
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

terminal = {
    'paygent' :  {
                     'sn'    : '900123123456456',
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
                     'sn'    : '701692349383826',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000100001'
                 },
    'gmo-pg' :   {
                     'sn'    : '316501470337677',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000500007'
                 },
    'pay-jp' :   {
                     'sn'    : '334714378614310',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000003300002'
                 },
    'sony' :     {
                     'sn'    : '778505488804181',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000200001'
                 },
    'rakuten' :  {
                     'sn'    : '000118183306329',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000002700011'
                 },
    'sbps' :     {
                     'sn'    : '916501470337654',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000003600001'
                 },
    'smbc-fs' :  {
                     'sn'    : '664498427667744',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000600001'
                 },
    'smbc-gmo' : {
                     'sn'    : '533587303990544',
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
                     'sn'    : '499327392827577',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000000800001'
                 },
    'gmo-mb' :   {
                     'sn'    : '982434646378875',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000001000001'
                 },
    'nicos-pg' :   {
                     'sn'    : '334714378614308',
                     'iv'    : 'cc7b9247ed6f8f7c41e9dcce0d340ef4',
                     'sver'  : '1000',
                     'ttyid' : '0000004200002'
                 },
}

