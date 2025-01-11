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

def int_cube_root(n):
    """
    Calculate integer cube root of a number using Newton's method.
    Returns the largest integer k such that k^3 <= n.
    
    Args:
        n (int): Number to find cube root of
        
    Returns:
        int: Integer cube root
    """
    if n < 0:
        return -int_cube_root(-n)
    if n == 0:
        return 0
    
    # Initial guess
    x = n
    
    # Newton's method iteration
    while True:
        new_x = (2 * x + n // (x * x)) // 3
        if new_x >= x:
            return x
        x = new_x

n = 17258212916191948536348548470938004244269544560039009244721959293554822498047075403658429865201816363311805874117705688359853941515579440852166618074161313773416434156467811969628473425365608002907061241714688204565170146117869742910273064909154666642642308154422770994836108669814632309362483307560217924183202838588431342622551598499747369771295105890359290073146330677383341121242366368309126850094371525078749496850520075015636716490087482193603562501577348571256210991732071282478547626856068209192987351212490642903450263288650415552403935705444809043563866466823492258216747445926536608548665086042098252335883
e = 3
ct = 243251053617903760309941844835411292373350655973075480264001352919865180151222189820473358411037759381328642957324889519192337152355302808400638052620580409813222660643570085177957
"""
This is typical RSA encryption with e = 3.
ct = pt^3 mod n
But the encrypted message is much shorter than the modulus n and without padding so modulus n is not involved in calculation. 
So we can easily decrypt it by taking the cube root of the ciphertext.
"""

from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

x = int_cube_root(ct)
pt = long_to_bytes(x)
print(pt)
e = 3
d = -1

noinverse = 0
while d == -1:
    p = getPrime(1024)
    q = getPrime(1024)
    phi = (p - 1) * (q - 1)
    print(f"p = {p}")
    print(f"q = {q}")
    try:
        d = inverse(e, phi)
    except ValueError:
        noinverse += 1
        d = -1
print (f'No inverse {noinverse} times')
# n = p * q

flag = b"XXXXXXXXXXXXXXXXXXXXXXX"
pt = bytes_to_long(flag)
ct = pow(pt, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")

pt = pow(ct, d, n)
decrypted = long_to_bytes(pt)
assert decrypted == flag


