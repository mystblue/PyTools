# -*- coding: utf-8 -*-

import json
import os
import sys

file_path = "gmo-mb_test.json"

error_list = [
    'gmo-mb-73901',
    'gmo-mb-74011',
    'gmo-mb-74563',
    'gmo-mb-74706',
    'gmo-mb-74945',
    'gmo-mb-75007',
    'gmo-mb-75079',
    'gmo-mb-75114',
    'gmo-mb-75151',
    'gmo-mb-75317',
    'gmo-mb-75389',
    'gmo-mb-75629',
    'gmo-mb-75701',
    'gmo-mb-75848',
    'gmo-mb-75918',
    'gmo-mb-76195',
    'gmo-mb-76373',
    'gmo-mb-76445',
    'gmo-mb-76481',
    'gmo-mb-76866',
    'gmo-mb-76938',
    'gmo-mb-77455',
    'gmo-mb-77492',
    'gmo-mb-77525',
    'gmo-mb-77840',
    'gmo-mb-77948',
    'gmo-mb-78053',
    'gmo-mb-78390',
    'gmo-mb-78462',
    'gmo-mb-78605',
    'gmo-mb-78768',
    'gmo-mb-78775',
    'gmo-mb-78977',
    'gmo-mb-79052',
    'gmo-mb-79184',
    'gmo-mb-79399',
    'gmo-mb-79578',
    'gmo-mb-79760',
    'gmo-mb-79832',
    'gmo-mb-79867',
    'gmo-mb-79928',
    'gmo-mb-80072',
    'gmo-mb-80213',
    'gmo-mb-80346',
    'gmo-mb-80420',
    'gmo-mb-80491',
    'gmo-mb-80551',
    'gmo-mb-80801',
    'gmo-mb-80861',
    'gmo-mb-81030',
    'gmo-mb-81102',
    'gmo-mb-81140',
    'gmo-mb-81343',
    'gmo-mb-81486',
    'gmo-mb-81521',
    'gmo-mb-81547',
    'gmo-mb-81620',
    'gmo-mb-81656',
    'gmo-mb-81954',
    'gmo-mb-82097',
    'gmo-mb-82268',
    'gmo-mb-82303',
    'gmo-mb-82482',
    'gmo-mb-82555',
    'gmo-mb-82590',
    'gmo-mb-82759',
    'gmo-mb-82892',
    'gmo-mb-82902',
    'gmo-mb-83071',
    'gmo-mb-83108',
    'gmo-mb-83179',
    'gmo-mb-83285',
    'gmo-mb-83288',
    'gmo-mb-83610',
    'gmo-mb-83778',
    'gmo-mb-83813',
    'gmo-mb-84019',
    'gmo-mb-84223',
    'gmo-mb-84331',
    'gmo-mb-84425',
    'gmo-mb-84500',
    'gmo-mb-84871',
    'gmo-mb-84967',
    'gmo-mb-85002',
    'gmo-mb-85232',
    'gmo-mb-85265',
    'gmo-mb-85409',
    'gmo-mb-85434',
    'gmo-mb-85747',
    'gmo-mb-86081',
    'gmo-mb-86117',
    'gmo-mb-86489',
    'gmo-mb-86552',
    'gmo-mb-86863',
    'gmo-mb-86869',
    'gmo-mb-86935',
    'gmo-mb-86970',
    'gmo-mb-87186',
    'gmo-mb-87461',
    'gmo-mb-87559',
    'gmo-mb-87689',
    'gmo-mb-87752',
    'gmo-mb-87787',
    'gmo-mb-87955',
    'gmo-mb-88027',
    'gmo-mb-88051',
    'gmo-mb-88087',
    'gmo-mb-88256',
    'gmo-mb-88290',
    'gmo-mb-88327',
    'gmo-mb-88362',
    'gmo-mb-88399',
    'gmo-mb-88435',
    'gmo-mb-88469',
    'gmo-mb-89984',
    'gmo-mb-90392',
    'gmo-mb-90870',
    'gmo-mb-90932',
    'gmo-mb-91099',
    'gmo-mb-91229',
    'gmo-mb-91265',
    'gmo-mb-91650',
    'gmo-mb-91783',
    'gmo-mb-91817',
    'gmo-mb-91880',
    'gmo-mb-92012',
    'gmo-mb-92252',
    'gmo-mb-92347',
    'gmo-mb-92357',
    'gmo-mb-92645',
    'gmo-mb-92743',
    'gmo-mb-93079',
    'gmo-mb-93115',
    'gmo-mb-93559',
    'gmo-mb-93665',
    'gmo-mb-94254',
    'gmo-mb-94256',
    'gmo-mb-94290',
    'gmo-mb-94517',
    'gmo-mb-94818',
    'gmo-mb-95131',
    'gmo-mb-95262',
    'gmo-mb-95334',
    'gmo-mb-95466',
    'gmo-mb-95563',
    'gmo-mb-95635',
    'gmo-mb-95671',
    'gmo-mb-95839',
    'gmo-mb-95909',
    'gmo-mb-96007',
    'gmo-mb-96282',
    'gmo-mb-96355',
    'gmo-mb-96571',
    'gmo-mb-96679',
    'gmo-mb-96812',
    'gmo-mb-96977',
    'gmo-mb-97015',
    'gmo-mb-97148',
    'gmo-mb-97255',
    'gmo-mb-97278',
    'gmo-mb-97386',
    'gmo-mb-97421',
    'gmo-mb-97447',
    'gmo-mb-97482',
    'gmo-mb-97553',
    'gmo-mb-97712',
    'gmo-mb-98168',
    'gmo-mb-98587',
    'gmo-mb-98683',
    'gmo-mb-98719',
    'gmo-mb-98946',
    'gmo-mb-99113',
    'gmo-mb-99115',
    'gmo-mb-99377',
    'gmo-mb-99413'
]

def test():
    buf = ""
    with open(file_path, "r", encoding="utf-8") as f:
        buf = f.read()
    json_obj = json.loads(buf)
    
    ret = []
    for test in json_obj:
        if test["testNo"] in error_list:
            ret.append(test)
        
    with open("gmo_mb_error.json", "w", encoding="utf-8") as fw:
        fw.write(json.dumps(ret, ensure_ascii=False))

if __name__ == '__main__':
    test()