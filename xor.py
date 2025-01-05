from Crypto.Util.number import *
"""
https://cryptohack.org/courses/intro/xor0/

XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise. 
In textbooks the XOR operator is denoted by ⊕, but in most challenges and programming languages you will see the caret ^ used instead.
"""
def xor(text, key):


    ret = str()    
    for c in text:
        if not c.isprintable():
            raise ValueError("Invalid text")
        ret += chr(ord(c) ^ key)
        
    return ret

b = "label"
k = 13

print(xor(b,k))

