


def baby_step_giant_step(p, a, G_x, A_x):
    def point_add(x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            # Point doubling
            m = (3 * x1**2 + a) * pow(2*y1, -1, p)
        else:
            # Point addition
            m = (y2 - y1) * pow(x2 - x1, -1, p)
        m %= p
        x3 = (m**2 - x1 - x2) % p
        y3 = (m * (x1 - x3) - y1) % p
        return x3, y3

    def point_mult(x, y, n):
        rx, ry = None, None
        while n:
            if n & 1:
                if rx is None:
                    rx, ry = x, y
                else:
                    rx, ry = point_add(rx, ry, x, y)
            x, y = point_add(x, y, x, y)
            n >>= 1
        return rx, ry

    # Compute square root of order
    m = int(p**0.5) + 1

    # Precompute baby steps
    baby_steps = {}
    x, y = find_y(G_x)
    baby_point = 1, G_x, y
    for i in range(m):
        baby_steps[baby_point[1]] = i
        baby_point = point_add(baby_point[0], baby_point[1], G_x, y)

    # Compute giant steps
    factor = point_mult(G_x, y, m)
    x, y = find_y(A_x)
    for j in range(m):
        check_x = (x - factor[0] * j) % p
        if check_x in baby_steps:
            return baby_steps[check_x] + j * m

    return None

def find_y(x):
    p = 310717010502520989590157367261876774703
    a, b = 2, 3
    # Solve y² = x³ + ax + b mod p using Tonelli-Shanks
    def legendre(a, p):
        return pow(a, (p - 1) // 2, p)

    if legendre(x**3 + a*x + b, p) != 1:
        return None

    def mod_sqrt(a, p):
        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)
        
        # More complex Tonelli-Shanks implementation if needed
        # This is simplified and might not work for all primes
        q = p - 1
        s = 0
        while q % 2 == 0:
            q //= 2
            s += 1
        
        z = 2
        while legendre(z, p) != -1:
            z += 1
        
        c = pow(z, q, p)
        r = pow(a, (q + 1) // 2, p)
        t = pow(a, q, p)
        m = s
        
        while t != 1:
            i = 0
            tmp = t
            while tmp != 1:
                tmp = (tmp * tmp) % p
                i += 1
                if i == m:
                    return None
            
            b = pow(c, 1 << (m - i - 1), p)
            r = (r * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i
        
        return r

    y = mod_sqrt(x**3 + a*x + b, p)
    return x, y

from sagemath import *
from math import ceil, sqrt
def bsgs_ecdlp(P, Q, E):
    if Q == E((0, 1, 0)):
        return P.order()
    if Q == P:
        return 1
    m = ceil(sqrt(P.order()))
    # Baby Steps: Lookup Table
    lookup_table = {j*P: j for j in range(m)}
    # Giant Step
    for i in range(m):
        temp = Q - (i*m)*P
        if temp in lookup_table:
            return (i*m + lookup_table[temp]) % P.order()
    return None




# Solve the specific challenge
p = 310717010502520989590157367261876774703
a = 2
b = 3
G_x = 179210853392303317793440285562762725654
A_x = 280810182131414898730378982766101210916

n = baby_step_giant_step(p, a, G_x, A_x)
print(f"Discrete logarithm n = {n}")