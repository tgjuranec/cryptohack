import hashlib
from random import randint
from Crypto import *
from Crypto.Util.number import *
import json


def gcd(a, b):
    remainders = [a,b]
    while b != 0:
        atmp = a
        btmp = b
        b = atmp%btmp
        remainders.append(b)
        a = btmp
    return remainders

def extended_gcd(a, b):    
    remainders = gcd(a,b)
    i = len(remainders)-1
    xtmp = 0
    ytmp = 1  
    while i > 0:
        i -= 1
        x = ytmp - (remainders[i-1] // remainders[i])*xtmp
        y = xtmp
        xtmp = x
        ytmp = y
    return x,y

def qresidue_legrende(n, p):
    """
    Quadratic Residue using Legrende Symbol
    :param n: integer
    :param p: prime number - modules
    :return: 1 if n is a quadratic residue modulo p, -1 if n is a non-residue modulo p, 0 if n ≡ 0 (mod p)
    """
    ex = (p-1)//2
    a = pow(n, ex,p)

    if a == 1:
        return 1
    elif a == p-1:
        return -1
    else:
        return 0
    
"""



"""


def chinese_remainder_theorem(a, b, p, q):
    """
    Chinese Remainder Theorem
    :param a: integer
    :param b: integer
    :param p: prime number
    :param q: prime number
    :return: x
    """
    N = p*q
    M1 = N//p
    M2 = N//q
    M1_inv, _ = extended_gcd(M1, p)
    M2_inv, _ = extended_gcd(M2, q)
    x = (a*M1*M1_inv + b*M2*M2_inv) % N
    return x

def sha256(message)->str:
    """
    SHA256
    :param message: string
    :return: hash
    """
    return hashlib.sha256(message.encode()).hexdigest()

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os



def encrypt_flag(shared_secret: int):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    # Prepare data to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data

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
        return  plaintext.decode('ascii')
    

import socket

HOST = "socket.cryptohack.org"
PORT = 13371
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST,PORT))


send_string_init = '{"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0xd31eb8cf8bc053e138f99c8d488e312b6cb9036699734150abc070cd2489d984a33a6edb7b4996fee67ad960e8b596d4498d4428b54f4f079635513925153ca3c29e3f73cf3323140a623ae049c758ffe0216ba78082950f771eddef6a1b8ef9fbfcd4eb7fc53e70d025c61bb242035a52cfd5ea685e87850929cc37b474fa577ed85c10cc9f7e48582dc209ff3ee8880af148608f2cadfa016681d2882ee4b5815fafa6b985fe150e59d97265a02e3e9a24d2aaa29ecc2035504bf08b8b175d"}'
# sock.sendall(send_string_init.encode())

# RECEIVED FROM ALICE 
# jsonstringA = '{"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0x3586aed0de267ca203d04fb3998858184ab4e42c3d669723f519b8a0167fe38ea0e062030e888f33f44aedbbd23ecaa12beb731581a11f8288eb3ae61524abab5cfc858d20073b01a201544d08f1e660339f03642c027be6eef1d2cc518b3052bbe7977689c91612d39f57ca9861da206b549f68f77e236cd6213d2cdf09905183a5951cdb66968a1f767ba0e936f3383d81b2f999a45d4c9c873d3ede86c1187e18db3319dbf3fb6a036d37500cd3a741e962359b231c44a0a27f24082f996d"}'


input = sock.recv(2048).decode("ascii")
print(input)
sock.sendall(send_string_init.encode())
input = sock.recv(2048).decode("ascii")
print(input)
jsonstringA = input[input.find("{"):input.find("}")+1]
jsondataA = json.loads(jsonstringA)
p = int(jsondataA['p'], 16)
g = int(jsondataA['g'], 16)
A = int(jsondataA['A'], 16)
# CREATE A FAKE PRIVATE KEY FOR COMMUNICATION WITH ALICE!!!
bfake = 333930369188680653901414021193501082933468091819283816669584810395166174808302943255462316998695156419180731436157472105378630043018086278586683863706286109613420712607996668419148638810498417062689558428013085174438528226046603670388918919373717415640051551773140685483832440550029001834316040395694753459757921160169976415556998386813135879261018474231015132847802876386310312997724996443102630178291977930488943955806884736516494900888414493843880549405227938
if(bfake >= p): bfake = p-2
# print(f'bfake = {bfake}')
Bfake = pow(g,bfake, p)
shared_secret_Bfake = pow(A,bfake,p)

jsonstringB = '{"B": "0xb4f0c5c303578957d69ce94b4f4eef9cedd4d648aea6c1ba0bc11a8cd65032e56c4a6f1f0e17c263d0d86cbaa244776a435c4f2aaaacd1b93c23db98b915ccb8002952083e9b11c8e22cd7ca96838d9b24b5a7ab8d8d3b47d27ae14c429508d758d01b018ea53b2a38317a18d364169b5fe8fac88e98205d78b115aeb705b2b4113829d4db2c95bfca66fa53b08cd4ca3fa56096da01b95d053b019391bf837b2725c50757bdae517fed8fcc5507ec4b9e5ea9e3d0bc13731e8e2a25c8577813"}'
# input = sock.recv(2048).decode("ascii")
# jsonstringB = input[input.find("{"):input.find("}")+1]
jsondataB = json.loads(jsonstringB)
B = int(jsondataB['B'],16)
jsondataBfake = jsondataB.copy()
jsondataBfake['B'] = hex(Bfake)
send_stringALICE= json.dumps(jsondataBfake)
sock.sendall(send_stringALICE.encode()) 



# CREATE A FAKE PRIVATE KEY FOR COMMUNICATION WITH BOB!!!
afake = 83315473272357384846570709455750312386225469842831224928636409015704267958037525939485821431421825479524711877005780064113698383460922919114931098064702502903228347408054855035492687899656552806152380394348194067436194413367252284496170938543304518408263049666989201917305500664843267047065108125234703181158480009562477273093056645398026223021207081954979927382393897970209481340825675244445627700451420913968792083491113709154958397221963754436009983505881762
if(afake >= p): afake = p-2
Afake = pow(g, afake, p)
shared_secret_Afake = pow(A, afake, p)
jsondataAfake = jsondataA.copy()
jsondataAfake['A'] = hex(Afake)
send_stringBOB = json.dumps(jsondataAfake)
sock.sendall(send_stringALICE.encode())

input = str(sock.recv(2048),"ascii")
print(input)
if input.find('encrypted_flag') == -1:
    sock.sendall(send_stringALICE.encode())
    input = str(sock.recv(2048),"ascii")
    print(input)
# last received string consists of:
# - Intercepted from Bob: {"B": ...}\n Intercepted from Alice: {"iv": "...", "encrypted_flag": "..."}\n'
string_result = input[input.rfind("{"):input.rfind("}",)+1]
jsonResult = json.loads(string_result)
iv = jsonResult['iv']
encrypted_flag = jsonResult['encrypted_flag']

print(decrypt_flag(shared_secret_Bfake, iv,encrypted_flag))



pass



