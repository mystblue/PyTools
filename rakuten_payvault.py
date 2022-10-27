import datetime
from pytz import timezone
import requests
import json

# pip install pytz

#加盟店情報を設定
sid = "stg-rcjp-test"
key = "C372E7021F7CA2A1E1C3C9258CF99220435B03089E438DB20C8C5FDC45297C8C"

# 現在時刻を設定
dtime = datetime.datetime.now().astimezone(timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S.000')
data = {
	"serviceId": sid,
	"timestamp": dtime,
	"fullCardDetails": {
		"cardNumber": "5279000000000003",
		"expirationMonth": "01",
		"expirationYear": "2027",
		"cvv": "777"
	}
}
# リクエストパラメータをJSON形式の文字列として設定
jsonData = json.dumps(data)

# ヘッダーを設定
headers = {
	"Content-Type": "application/json;charset=utf-8"
}

print("PayVault V3/Add API Request: ")
print(jsonData)

url = "https://payvault-stg.global.rakuten.com/api/pv/Card/V3/Add"

res = requests.post(url, jsonData, headers).json()

print("PayVault V3/Add API Response: ")
print(res)