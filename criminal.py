from typing import Optional
import random
from Crypto.Util.number import *
import math

def is_prime(n: int, k: int = 5) -> bool:
    """
    Miller-Rabin primality test
    k determines the accuracy of the test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0:
        return False

    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def legendre_symbol(a: int, p: int) -> int:
    """
    Optimized Legendre symbol calculation for large numbers
    """
    if a == 0:
        return 0
    
    # Ensure a is in proper range
    a = a % p
    
    # Use quadratic reciprocity law for optimization
    result = pow(a, (p - 1) // 2, p)
    return -1 if result == p - 1 else result

def tonelli_shanks(n: int, p: int) -> Optional[int]:
    """
    Optimized Tonelli-Shanks for large integers
    """
    # Input validation
    if not is_prime(p):
        raise ValueError("p must be prime")
    if p < 2:
        raise ValueError("p must be greater than 2")
    
    # Check if n is actually a quadratic residue
    if legendre_symbol(n, p) != 1:
        return None
    
    # Ensure n is in proper range
    n = n % p
    
    # Simple case for p ≡ 3 (mod 4)
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    
    # Factor out powers of 2 from p-1
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    
    # Find quadratic non-residue using randomization for efficiency
    z = 2
    while legendre_symbol(z, p) != -1:
        z = random.randrange(2, p)
    
    # Initialize variables
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    
    # Main loop with optimized modular arithmetic
    while t != 1:
        # Find least i such that t^(2^i) ≡ 1 (mod p)
        i = 0
        temp = t
        while temp != 1 and i < m:
            temp = pow(temp, 2, p)  # Using pow() instead of multiplication
            i += 1
            
        if i == m:
            return None
        
        # Update variables using efficient modular exponentiation
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
    
    return r

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
"""

The Elliptic Curve Diffie-Hellman Key Exchange goes as follows:

    Alice generates a secret random integer nA and calculates QA=[nA]G
    Bob generates a secret random integer nB and calculates QB=[nB]G
    Alice sends Bob QA and Bob sends Alice QB. Due to the hardness of ECDLP, an onlooker Eve is unable to calculate nA/BnA/B in reasonable time.
    Alice then calculates [nA]QB, and Bob calculates [nB]QA.
    Due to the associativity of scalar multiplication, S=[nA]QB=[nB]QA.
    Alice and Bob can use S as their shared secret.
"""

from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib
import os

# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'

FLAG = b'crypto{??????????????????????????????}'


def check_point(P: tuple):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P: tuple, Q: tuple):
    # based of algo. in ICM
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R


def double_and_add(P: tuple, n: int):
    # based of algo. in ICM
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R


def gen_shared_secret(Q: tuple, n: int):
    # Bob's Public key, my secret int
    S = double_and_add(Q, n)
    return S.x


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


# Define the curve
p = 310717010502520989590157367261876774703
a = 2
b = 3
if isPrime(p):
    print("Prime")
# Generator
g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
G = Point(g_x, g_y)

# My secret int, different every time!!
n = randint(1, p)

# Send this to Bob!
qa = double_and_add(G, n)
print(qa)

# Bob's public key
qb_x = 272640099140026426377756188075937988094
qb_y = 51062462309521034358726608268084433317
B = Point(qb_x, qb_y)

# Calculate Shared Secret
shared_secret = gen_shared_secret(B, n)

# Send this to Bob!
ciphertext = encrypt_flag(shared_secret)
print(ciphertext)

qa_output = Point(280810182131414898730378982766101210916, 291506490768054478159835604632710368904)
qx = G
i = 400000000
while i < 500000000:
    i += 1
    qx = point_addition(qx, G)
    if qx[0] == qa_output[0]:
        print(f"Found n: {i} - {qx}")
        break



a = {'iv': '07e2628b590095a5e332d397b8a59aa7', 'encrypted_flag': '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'}

