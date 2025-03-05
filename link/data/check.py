
def get_tty_id(str):
    index1 = str.find("POI端末トランザクションID")
    index2 = str.find("要求処理カテゴリ")
    return str[index1 + len("POI端末トランザクションID"):index2]

def get_request_date(str):
    index1 = str.find("処理区分端末リクエスト日時")
    index2 = str.find("レスポンス日時")
    return str[index1 + len("処理区分端末リクエスト日時"):index2]
    
def get_sl_code(str):
    index1 = str.find("加盟店コード")
    index2 = str.find("端末シリアル番号")
    return str[index1 + len("加盟店コード"):index2]
    
def get_merchant_name(str):
    index1 = str.find("加盟店コード")
    index2 = str.find("端末シリアル番号")
    return str[index1 + len("加盟店コード"):index2]
    
def get_sn(str):
    index1 = str.find("端末シリアル番号")
    index2 = str.find("端末ID")
    return  str[index1 + len("端末シリアル番号"):index2]
    
def get_psp(str):
    index1 = str.find("決済代行事業者略称")
    index2 = str.find("加盟店コード")
    return str[index1 + len("決済代行事業者略称"):index2]
    
def get_result(str):
    index1 = str.find('"mstatus":"')
    temp = str[index1 + len('"mstatus":"'):]
    index2 = temp.find('"')
    return temp[:index2]
    
def get_request(str):
    index1 = str.find("その他リクエスト項目")
    index2 = str.find("応答処理結果コード")
    return str[index1 + len("その他リクエスト項目"):index2]
    
def get_response(str):
    index1 = str.find("その他レスポンス項目")
    index2 = str.find("トレース情報登録ホスト")
    return str[index1 + len("その他レスポンス項目"):index2]
    
def main(filename):
    print("■" + filename)
    buf = ''
    with open(filename, "r", encoding="utf-8") as f:
        buf = f.read()
    
    lines = buf.split('\n')
    
    ret = ""
    
    for i in range(1, len(lines)-1):
        if lines[i] == '':
            continue
        if lines[i].startswith('SL'):
            continue
        if lines[i].startswith('処理区分端末リクエスト日時'):
            tty_id = get_tty_id(lines[i])
            request_date = get_request_date(lines[i])
            sl_code = get_sl_code(lines[i])
            sn = get_sn(lines[i])
            psp = get_psp(lines[i])
            result = get_result(lines[i])
            request = get_request(lines[i])
            response = get_response(lines[i])
            ret += tty_id + "\t" + request_date + "\t" + sl_code + "\t\t" + sn + "\t" + psp + "\t" + result + "\t\t" + request + "\t" + response + "\n"

    with open("result.csv", "w", encoding="utf-8") as f:
        f.write(ret)

if __name__ == '__main__':
    main("test.txt")
