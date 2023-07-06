from Crypto.Cipher import AES
from Crypto.Util import Padding
import base64

targetText = "暗号化された文字列"

key = bytes("12345678abcdefgh", 'utf-8')
iv = bytes("12345678abcdefgh", 'utf-8')

aes = AES.new(key, AES.MODE_CBC, iv)
data = Padding.pad(targetText.encode('utf-8'), AES.block_size, 'pkcs7')
encrypted = aes.encrypt(data)
print(encrypted)
print(base64.b64encode(encrypted))