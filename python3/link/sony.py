# -*- coding: utf-8 -*-
import json
import os
TEST = """{
        "testNo": "sony-0001",
        "処理区分": "カード預かり登録",
        "区分": "正常系",
        "試験目的": "カード預かり更新用",
        "内容": "",
        "header": {
            "IV": "464720cd46a34e1ba499290182e964e9",
            "SN": "778505488804182",
            "header_error": "0",
            "Sver": "1000"
        },
        "request": {
            "defaultFlag": "0",
            "customerId": "",
            "category": 4,
            "ttyId": "0000001600001",
            "customerPass": "",
            "transactionDate": "{$TODAY}",
            "cardNumber": "4123000000000700",
            "cardExpire": "1228",
            "securityCode": "8888"
        },
        "response": {
            "mstatus": "success",
            "vResultCode": "",
            "merrMsg": "",
            "orderId": "",
            "resAuthCode": "",
            "gwErrCd": "",
            "gwErrMsg": "",
            "requestDate": "",
            "responseDate": "",
            "processId": "",
            "processPass": "",
            "merchantFree1": "",
            "merchantFree2": "",
            "merchantFree3": "",
            "mcSecCd": "",
            "mcKanaSei": "",
            "mcKanaMei": "",
            "mcBirthDay": "",
            "mcTelNo": "",
            "mcSex": "",
            "mcBirthYear": "",
            "mcPostal": "",
            "mcAcntNo1": "",
            "mcAcntNo2": "",
            "mcCardMei": "",
            "issurClass": "",
            "acqId": "",
            "acqName": "",
            "issurName": "",
            "issurId": "",
            "numOfCards": "",
            "customerCardId": "",
            "forward": "",
            "method": "",
            "payTimes": "",
            "tranDate": "",
            "checkString": "",
            "reqCardNumber": "",
            "transactionId": "",
            "customerId": "",
            "creditErrorCode": "",
            "reqId": "",
            "reqBrand": "",
            "reqExpireStatus": "",
            "billNumber": "",
            "token": "",
            "nameKana": "",
            "description": "",
            "email": "",
            "tel": "",
            "dateOfBirth": "",
            "zip": "",
            "line1": "",
            "line2": "",
            "brand": "",
            "last4": "",
            "expire": "",
            "cardTypeMsg": "",
            "cardKindCd": "",
            "formatType": "",
            "cardholderName": ""
        }
    }
"""
CUSTOMER_ID = "kEkU34CcXMMJ58780273885534714169A"
CUSTOMER_PASS = "028282923410"
def create_testcase():
    test_list = list()
    print(CUSTOMER_ID)
    print(CUSTOMER_PASS)
    t = json.loads(TEST)
    t["request"]["customerId"] = CUSTOMER_ID
    t["request"]["customerPass"] = CUSTOMER_PASS
    test_list.append(t)
        
    with open('sony_test.json', 'w', encoding="utf-8") as f:
        json.dump(test_list, f, ensure_ascii=False, indent=4)
if __name__ == '__main__':
    create_testcase()
