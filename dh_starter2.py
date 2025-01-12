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

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes


g = 7
p = 28151
d = dict()

for i in range(1, p):
    if d.get(pow(g,i,p)) is None:
        d[pow(g, i, p)] = list()
    d[pow(g, i, p)].append(i)

for i in range(1, p):
    if d.get(i) is not None and i < 1000:
        print(i, d[i])


# FIND THE SMALLEST PRIMITIVE ELEMENT WHICH GENERATES THE WHOLE FIELD FP
# THAT MEANS THE ORDER OF THE ELEMENT IS P-1: LEN(D) == P-1
for g in range(2, p):
    d = dict()
    for i in range(1, p):
        if d.get(pow(g,i,p)) is None:
            d[pow(g, i, p)] = list()
        d[pow(g, i, p)].append(i)
    if len(d) == p-1:
        print(g)
        break