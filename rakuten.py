
# ステージング環境
# https://payment-stg.global.rakuten.com/gp/Payment/V1/Authorize
# 本番環境
# https://payment.global.rakuten.com/gp/Payment/V1/Authorize

import datetime
from pytz import timezone
import requests
import json
import base64
import hashlib
import hmac
url = "https://payment-stg.global.rakuten.com/gp/Payment/V1/Authorize"
kv = "1"
# 貴社の情報を設定
sid = "stg-rcjp-test"
key = "C372E7021F7CA2A1E1C3C9258CF99220435B03089E438DB20C8C5FDC45297C8C"
pid = "123"
# 現在時刻を設定
#time = datetime.datetime.now().astimezone(timezone('UTC')).strftime('%Y --%m --%d %H:%M:%S.
time = datetime.datetime.now().astimezone(timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S.000')
#time = "2022-10-27 11:38:17.123"
print("time: " + time)
req = {
    "serviceId": sid,
    "subServiceId": sid,
    "paymentId": pid,
    "serviceReferenceId": "123",
    "timestamp": time,
    "agencyCode": "rakutencard",
    "cardToken": {
        "amount": "100",
        "cardToken": "2210270200162Ux9pqZsCOYpoQIv0003",
        "version": "2",
        "withThreeDSecure": "false"

    },
    "currencyCode": "JPY",
    "custom": "",
    "grossAmount": "100",
    "order": {
        "email": "rakuten@card",
        "ipAddress": "123.4.5.6",
        "version": "1"
    }
}

# リクエストパラメータを JSON 形式の文字列として設定
reqstr = json.dumps(req)
print("reqinfo: " + reqstr)

# JSON 形式のリクエストパラメータを Ba se64 でエンコード
reqenc = base64.b64encode(reqstr.encode())
print("reqenc: " + reqenc.decode('utf 8'))

# 認証キーを 使用して HMAC によりハッシュを生成（デジタル署名として設定するため）
sig = hmac.new(key.encode("utf 8"), reqstr.encode("utf 8"), hashlib.sha256).hexdigest()
print("sig: " + sig)
data = {"paymentinfo": reqenc, "signature": sig, "key_version": kv}
res = requests.post(url, data).json()
print("res: ")
print(res)