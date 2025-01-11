import hashlib
from random import randint
from Crypto import *
from Crypto.Util.number import *


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

n = 110581795715958566206600392161360212579669637391437097703685154237017351570464767725324182051199901920318211290404777259728923614917211291562555864753005179326101890427669819834642007924406862482343614488768256951616086287044725034412802176312273081322195866046098595306261781788276570920467840172004530873767                                                                  
e = 1  # public key is 1 
ct = 44981230718212183604274785925793145442655465025264554046028251311164494127485

"""

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

e = 1
d = -1

while d == -1:
    p = getPrime(512)
    q = getPrime(512)
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

n = p * q

flag = b"XXXXXXXXXXXXXXXXXXXXXXX"
pt = bytes_to_long(flag)
ct = pow(pt, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

pt = pow(ct, d, n)
decrypted = long_to_bytes(pt)
assert decrypted == flag


"""
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# private key is 1

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")
d = 1
# all inverse functions returns 1 if e is 1 !!!!!!!!!!!!
d1 = inverse(e, n)
d2 = extended_gcd(e, n)[0]
pt = pow(ct, d, n)
decrypted = long_to_bytes(pt)
print(decrypted)

assert decrypted == flag
