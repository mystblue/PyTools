from Crypto.Cipher import AES
from Crypto.Util import Padding
import base64

targetText = "NxDoefMgm4/jlnXFcH/9JqWPVmntsZ1+TqD0rOLYwyo="

text = base64.b64decode(targetText)
print(text)

key = bytes("12345678abcdefgh", 'utf-8')
iv = bytes("12345678abcdefgh", 'utf-8')

aes = AES.new(key, AES.MODE_CBC, iv)
plaintext = aes.decrypt(text)
print(plaintext.decode(encoding='utf-8'))
