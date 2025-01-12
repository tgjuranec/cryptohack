import hashlib
from random import randint
from Crypto import *
from Crypto.Util.number import *

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

def derive_aes_key(dh_shared_secret, salt=None):
    # Use HKDF to derive a suitable AES key from the DH shared secret
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # For AES-256
        salt=salt,
        info=b'handshake data',
        backend=default_backend()
    )
    
    aes_key = hkdf.derive(dh_shared_secret)
    return aes_key


def decrypt_aes_256(encrypted_hex, key, iv_hex):
    # Convert hex strings to bytes
    ciphertext = binascii.unhexlify(encrypted_hex)
    iv = binascii.unhexlify(iv_hex)
    
    # Create cipher object
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    
    # Create decryptor
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding (PKCS7)
    padding_length = decrypted_padded[-1]
    decrypted = decrypted_padded[:-padding_length]
    
    return decrypted

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes


g = 2
p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919 
# a = 
# A = pow(g, a, p)

A = 112218739139542908880564359534373424013016249772931962692237907571990334483528877513809272625610512061159061737608547288558662879685086684299624481742865016924065000555267977830144740364467977206555914781236397216033805882207640219686011643468275165718132888489024688846101943642459655423609111976363316080620471928236879737944217503462265615774774318986375878440978819238346077908864116156831874695817477772477121232820827728424890845769152726027520772901423784 

 
b = 197395083814907028991785772714920885908249341925650951555219049411298436217190605190824934787336279228785809783531814507661385111220639329358048196339626065676869119737979175531770768861808581110311903548567424039264485661330995221907803300824165469977099494284722831845653985392791480264712091293580274947132480402319812110462641143884577706335859190668240694680261160210609506891842793868297672619625924001403035676872189455767944077542198064499486164431451944
B = 1241972460522075344783337556660700537760331108332735677863862813666578639518899293226399921252049655031563612905395145236854443334774555982204857895716383215705498970395379526698761468932147200650513626028263449605755661189525521343142979265044068409405667549241125597387173006460145379759986272191990675988873894208956851773331039747840312455221354589910726982819203421992729738296452820365553759182547255998984882158393688119629609067647494762616719047466973581

# S1 = pow(B, a, p)
S2 = pow(A, b, p)
IV = "737561146ff8194f45290f5766ed6aba"
ENCRYPTED_FLAG = "39c99bf2f0c14678d6a5416faef954b5893c316fc3c48622ba1fd6a9fe85f3dc72a29c394cf4bc8aff6a7b21cae8e12c"
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')




print(decrypt_flag(S2, IV, ENCRYPTED_FLAG))


