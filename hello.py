from Crypto.Util.number import *
"""
https://cryptohack.org/courses/intro/enc4/

Cryptosystems like RSA works on numbers, but messages are made up of characters. How should we convert our messages into numbers so that mathematical operations can be applied?

The most common way is to take the ordinal bytes of the message, convert them into hexadecimal, and concatenate. This can be interpreted as a base-16/hexadecimal number, and also represented in base-10/decimal.

To illustrate:

message: HELLO
ascii bytes: [72, 69, 76, 76, 79]
hex bytes: [0x48, 0x45, 0x4c, 0x4c, 0x4f]
base-16: 0x48454c4c4f
base-10: 310400273487 



"""

strnum10 = "11515195063862318899931685488813747395775516287289682636499965282714637259206269"
# Conversion from big string to big int !!!! Python can handle big numbers!!!! Unbelievable!!!!
num10 = int(strnum10)
b = long_to_bytes(num10)

print(b)