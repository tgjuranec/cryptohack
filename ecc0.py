from typing import Optional
import random

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

def test_and_find_root(n: int, p: int) -> Optional[int]:
    """
    Test if n is a quadratic residue modulo p with input validation
    """
    # Input validation
    if not isinstance(n, int) or not isinstance(p, int):
        raise TypeError("Inputs must be integers")
    if p <= 0:
        raise ValueError("p must be positive")
    if not is_prime(p):
        raise ValueError("p must be prime")
    
    try:
        legendre = legendre_symbol(n, p)
        print(f"Legendre symbol ({n}|{p}) = {legendre}")
        
        if legendre == 0:
            print(f"{n} ≡ 0 (mod {p})")
            return 0
        elif legendre == -1:
            print(f"{n} is a quadratic non-residue modulo {p}")
            return None
        else:
            root = tonelli_shanks(n, p)
            print(f"{n} is a quadratic residue modulo {p}")
            print(f"Square root = {root}")
            return root
    except OverflowError:
        raise ValueError("Input numbers too large for computation")

p = 9739
x = 8045
ysquare = pow(x,3) + 497*x + 1768
if legendre_symbol(ysquare, p) == 1:
    y = tonelli_shanks(ysquare,p)
    print(y)



