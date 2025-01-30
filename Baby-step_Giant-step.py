import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
import random
from Crypto.Util.number import *

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# Define the SECP256K1 curve parameters
curve = {
    'p': 310717010502520989590157367261876774703,
    'a': 2,
    'b': 3
}

# Define the base point G on the elliptic curve
G_x = 179210853392303317793440285562762725654
G_y = 105268671499942631758568591033409611165

def ecdlp_solver(curve, G, public_key):
    """
    Solve the Elliptic Curve Discrete Logarithm Problem (ECDLP) using the Baby-step Giant-step algorithm.
    
    Parameters:
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).
    - G (tuple): The base point G on the elliptic curve as a tuple (x, y).
    - public_key (tuple): The public key point on the elliptic curve as a tuple (x, y).

    Returns:
    - k (int or None): The discrete logarithm k such that k*G = public_key, or None if no solution is found.
    """
    p = curve['p']
    m = math.isqrt(p) + 1  # Calculate the step size

    # Precompute baby steps
    baby_steps = {}
    for j in range(m):
        P = multiply_point(G, j, curve)
        baby_steps[P] = j

    # Compute the giant steps
    mG = multiply_point(G, m, curve)
    Q = public_key

    for i in range(m):
        if Q in baby_steps:
            return i * m + baby_steps[Q]
        Q = add_points(Q, (-mG[0] % p, -mG[1] % p), curve)  # Q - mG

    return None

def multiply_point(P, k, curve):
    """
    Multiply a point P by an integer k on the given elliptic curve using the double-and-add method.
    
    Parameters:
    - P (tuple): The point on the elliptic curve as a tuple (x, y).
    - k (int): The integer multiplier.
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).

    Returns:
    - Q (tuple): The resulting point after multiplication.
    """
    if k == 0:
        return (0, 0)
    elif k == 1:
        return P
    else:
        Q = multiply_point(P, k // 2, curve)
        Q = add_points(Q, Q, curve)
        if k % 2:
            Q = add_points(Q, P, curve)
        return Q

def add_points(P, Q, curve):
    """
    Add two points P and Q on the given elliptic curve.
    
    Parameters:
    - P (tuple): The first point on the elliptic curve as a tuple (x, y).
    - Q (tuple): The second point on the elliptic curve as a tuple (x, y).
    - curve (dict): Dictionary containing the parameters of the elliptic curve (p, a, b).

    Returns:
    - R (tuple): The resulting point after addition.
    """
    p = curve['p']
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        # Point doubling
        s = (3 * x1 * x1 + curve['a']) * pow(2 * y1, p-2, p) % p
    else:
        # Point addition
        s = (y2 - y1) * pow(x2 - x1, p-2, p) % p

    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


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

def tonelli_shanks(n: int, p: int) -> int:
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

# Input the uncompressed public key as a string
public_key = 280810182131414898730378982766101210916

# Parse the public key
x = public_key
y = tonelli_shanks((x**3 + curve['a']*x + curve['b']) % curve['p'], curve['p'])

# Call the ECDLP solver with the parsed public key
k = ecdlp_solver(curve, (G_x, G_y), (x, y))
print(f"Discrete logarithm: {k}")


