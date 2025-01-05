from Crypto.Util.number import *
import math as m

def qresidue(n, p):
    """
    Quadratic Residue
    :param n: integer
    :param p: prime number
    :return: True if n is a quadratic residue modulo p, False otherwise
    """
    for i in range(1,p):
        tmp = m.sqrt(i*p+n)
        if tmp.is_integer():
            return True
    
    return False


ints = [14,6,11]
for i in ints:
    print(qresidue(i, 29))
