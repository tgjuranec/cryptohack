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

print(extended_gcd(187,5))