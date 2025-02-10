import hashlib
import hmac
import time

def dynamic_truncate(digest_bytes: bytes) -> int:

    # 下位 4 ビットを offset とする
    # len(digest_bytes) == 20
    offset = digest_bytes[19] & 0xf

    # offset から 4 バイトの数値を得る
    binary = int.from_bytes(digest_bytes[offset : offset + 4], byteorder='big')

    # 符号有無の混乱を防ぐために最上位ビットを除外する
    binary_masked = binary & 0x7fffffff

    return binary_masked

def generate_hotp(seed: bytes, counter: bytes) -> str:

    digest_bytes = hmac.new(seed, counter, hashlib.sha1).digest()

    otp = dynamic_truncate(digest_bytes) % 1000000

    otp_string = str(otp).zfill(6)

    return otp_string


def get_current_unix_time() -> int:
    return int(time.time())

def get_current_steps() -> int:
    return int(get_current_unix_time() / 30)

def generate_totp(seed: bytes, steps: int) -> str:

    steps_bytes = steps.to_bytes(8, byteorder='big')

    otp_string = generate_hotp(seed, steps_bytes)

    return otp_string