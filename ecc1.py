from typing import Optional
import random
from Crypto.Util.number import *
import math


class Point:
    def __init__(self, x, y, a, b, p):
        """Initialize a point on curve y^2 = x^3 + ax + b (mod p)"""
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.p = p
        
        # Handle point at infinity
        if x is None and y is None:
            return
            
        # Verify the point lies on the curve
        if (y * y) % p != (x * x * x + a * x + b) % p:
            raise ValueError("Point is not on the curve")

    def __str__(self):
        if self.x is None:
            return "Point at infinity"
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        """Add two points on the same elliptic curve"""
        # Check if points are on the same curve
        if (self.a, self.b, self.p) != (other.a, other.b, other.p):
            raise ValueError("Points are not on the same curve")

        # Case 1: self is point at infinity
        if self.x is None:
            return other
            
        # Case 2: other is point at infinity
        if other.x is None:
            return self

        # Case 3: self and other have same x but different y (including y = 0)
        if self.x == other.x and self.y != other.y:
            return Point(None, None, self.a, self.b, self.p)  # Return point at infinity

        # Case 4: self == other, tangent line case
        if self == other:
            # Handle point of order 2 (where y = 0)
            if self.y == 0:
                return Point(None, None, self.a, self.b, self.p)
                
            # Compute slope of tangent line
            m = (3 * self.x * self.x + self.a) * pow(2 * self.y, -1, self.p) % self.p
            
        # Case 5: standard case, points are different and not vertical
        else:
            m = (other.y - self.y) * pow(other.x - self.x, -1, self.p) % self.p

        # Calculate new point coordinates
        x3 = (m * m - self.x - other.x) % self.p
        y3 = (m * (self.x - x3) - self.y) % self.p

        return Point(x3, y3, self.a, self.b, self.p)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.a == other.a and self.b == other.b and \
               self.p == other.p



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
    if(x < 0): return y
    return x


def addpoint(p,q,a,b, prime):
    """
    (a) If P=OP=O, then P+Q=QP+Q=Q.
    (b) Otherwise, if Q=OQ=O, then P+Q=PP+Q=P.
    (c) Otherwise, write P=(x1,y1)P=(x1,y1) and Q=(x2,y2)Q=(x2,y2).
    """
    if p[0] == q[0] and p[1] == -q[1]:
        return (0,0)
    else:
        l = 0
        if not (p[0] == q[0] and p[1] == q[1]):
            dy = q[1] - p[1]
            dx = q[0] - p[0]
            invmult = pow(dx,-1,prime)
            l= dy*invmult % prime
        if p[0] == q[0] and p[1] == q[1]:
            invmult = pow(2*p[1],-1, prime)
            l = (3*p[0]*p[0]+a)*invmult % prime
        x3 = (l*l - p[0] - q[0] ) % prime

        y3 = (l * (p[0] - x3) - p[1]) % prime
        return (x3,y3)

    pass



X=(5274,2841)
Y=(8669,740)
prime = 9739
ysquare = pow(X[0],3) + 497*X[0] + 1768
if legendre_symbol(ysquare, prime) == 1:
    y = tonelli_shanks(ysquare,prime)
    print(y)

print(addpoint(X,Y,497,1768,prime))
print(addpoint(X,X,497,1768,prime))

# Define the elliptic curve parameters
a = 497
b = 1768
p = 9739

# Define the points
P = Point(493,5564, a, b, p)
Q = Point(1539,4742, a, b, p)
O = Point(4403,5202, a, b, p)


# Add the points using the Point class
R = P + P
print(f"R = P + Q = {R}")

# Add the point to itself
S = Q+O
print(f"S = P + P = {S}")

T = R + S
print(f"T = R + S = {T}")
