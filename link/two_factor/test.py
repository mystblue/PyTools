import base64
import time
import hmac
import hashlib
 
time_step = 30

def dynamic_truncate(digest_bytes: bytes) -> int:
    """動的切り捨てする"""

    # 下位 4 ビットを offset とする
    # len(digest_bytes) == 20
    offset = digest_bytes[19] & 0xf

    # offset から 4 バイトの数値を得る
    binary = int.from_bytes(digest_bytes[offset : offset + 4], byteorder='big')

    # 符号有無の混乱を防ぐために最上位ビットを除外する
    binary_masked = binary & 0x7fffffff

    return binary_masked

def generate_hotp(seed: bytes, counter: bytes) -> str:
    """HOTP を計算する
       カウンタはビッグエンディアンで 8 バイト"""
    digest_bytes = hmac.new(seed, counter, hashlib.sha1).digest()
    otp = dynamic_truncate(digest_bytes) % 1000000
    otp_string = str(otp).zfill(6)
    return otp_string
    
# 
def get_current_unix_time() -> int:
    return int(time.time())

def get_current_steps() -> int:
    return get_current_unix_time() // time_step

def generate_totp(seed: bytes, steps: int) -> str:
    """TOTP を計算する"""
    steps_bytes = steps.to_bytes(8, byteorder='big')
    otp_string = generate_hotp(seed, steps_bytes)
    return otp_string

if __name__ == '__main__':
    print(generate_totp(base64.b32decode("H5GD2TKLKUUHASJUIZAW26REFM3HG5TH"), int(get_current_unix_time()/30)))
