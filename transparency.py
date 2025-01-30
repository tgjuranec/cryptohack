from Crypto.Util.number import *
import hashlib
import base64
from Crypto.PublicKey import RSA
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend

# a = RSA.import_key(open('bruce_rsa.pub').read())

# print(a.n)

cert_data = b''
with open('transparency.pem', 'rb') as key_file:
    key_data = key_file.read()

public_key = load_pem_public_key(key_data, default_backend())

key_info = {
    'key_type': type(public_key).__name__,
    'key_size': public_key.key_size
}

# Print key details
print(f"Key Type: {key_info['key_type']}")
print(f"Key Size: {key_info['key_size']} bits")

print(hex(public_key.public_numbers().n))
print(public_key.public_numbers().e)