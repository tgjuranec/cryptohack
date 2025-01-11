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

n = 171731371218065444125482536302245915415603318380280392385291836472299752747934607246477508507827284075763910264995326010251268493630501989810855418416643352631102434317900028697993224868629935657273062472544675693365930943308086634291936846505861203914449338007760990051788980485462592823446469606824421932591                                                                  
e = 65537
ct = 161367550346730604451454756189028938964941280347662098798775466019463375610700074840105776873791605070092554650190486030367121011578171525759600774739890458414593857709994072516290998135846956596662071379067305011746842247628316996977338024343628757374524136260758515864509435302781735938531030576289086798942  

# GET PRIVATE KEY  - N IS A MONOPRIME
d = extended_gcd(e, n-1)[0]
print(f'd: {d}')
pt = pow(ct, d, n)
print(f'pt: {pt}')
print(long_to_bytes(pt))

