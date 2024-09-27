import subprocess

list = [
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "DHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "DHE-RSA-CHACHA20-POLY1305",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "DHE-RSA-AES128-GCM-SHA256",
    "ECDHE-ECDSA-AES256-SHA384",
    "ECDHE-RSA-AES256-SHA384",
    "DHE-RSA-AES256-SHA256",
    "ECDHE-ECDSA-AES128-SHA256",
    "ECDHE-RSA-AES128-SHA256",
    "DHE-RSA-AES128-SHA256",
    "RSA-PSK-AES256-GCM-SHA384",
    "DHE-PSK-AES256-GCM-SHA384",
    "RSA-PSK-CHACHA20-POLY1305",
    "DHE-PSK-CHACHA20-POLY1305",
    "ECDHE-PSK-CHACHA20-POLY1305",
    "AES256-GCM-SHA384",
    "PSK-AES256-GCM-SHA384",
    "PSK-CHACHA20-POLY1305",
    "RSA-PSK-AES128-GCM-SHA256",
    "DHE-PSK-AES128-GCM-SHA256",
    "AES128-GCM-SHA256",
    "PSK-AES128-GCM-SHA256",
    "AES256-SHA256",
    "AES128-SHA256"

]

def curl(option):
    # curlコマンドを定義
    curl_command = [
        "curl",
        "-X", "POST",  # HTTPメソッド
        "-E", "./D19CF1C348EAB5AA.pem",
        #"--tlsv1.2", "--tls-max", "1.2",
        "--ciphers", option,
        "https://dev-gw-v2.paytg.jp",  # リクエストURL
    ]
    
    # subprocessでcurlコマンドを実行
    result = subprocess.run(curl_command, capture_output=True, text=True)
    
    # 結果を出力
    print("Response code:", result.returncode)
    print("Response body:", result.stdout)

def main():
    for item in list:
        print(item)
        print("\r\n")
        curl(item)

if __name__ == '__main__':
    main()
