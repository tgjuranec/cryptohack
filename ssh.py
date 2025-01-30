from Crypto.Util.number import *
import hashlib
import base64
from Crypto.PublicKey import RSA
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime


a = RSA.import_key(open('bruce_rsa.pub').read())

print(a.n)
"""
cert_data = b''
with open('c2048b-rsa-example-cert.der', 'rb') as cert_file:
    cert_data = cert_file.read()

cert = x509.load_der_x509_certificate(cert_data, default_backend())
print(cert.public_key().public_numbers().n)
"""