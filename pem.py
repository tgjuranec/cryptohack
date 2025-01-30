from Crypto.Util.number import *
import hashlib
import base64
from Crypto.PublicKey import RSA



a = RSA.import_key(open('privacy_enhanced_mail.pem').read())

print(a.d)