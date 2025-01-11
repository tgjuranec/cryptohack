from random import randint
from Crypto import *


a = 288260533169915
p = 1007621497415251


FLAG = b'crypto{????????????????????}'

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
    


def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)        
        if b == '1':
            ## qresidue here is '1' n= a^e mod p
            q = qresidue_legrende(n, p)            
            ciphertext.append(n)
        else:
            n = -n % p
            ## qresidue here is '-1' n= -a^e mod p
            q = qresidue_legrende(n, p)
            ciphertext.append(n)
        
    return ciphertext


print(encrypt_flag(FLAG))

# The flag is encrypted using the ElGamal cryptosystem. The public key is (a, p) = (288260533169915, 1007621497415251). The flag is encrypted bit by bit. If the bit is 1, the ciphertext is n = a^e mod p. If the bit is 0, the ciphertext is n = -a^e mod p. The ciphertext is the following:  