from Crypto.Util.number import *

"""
 KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf 

We don't need to convert the numbers to bytes because they are the same length so we can xor them directly

"""

KEY1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313

KEY2 = KEY1 ^ 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e

KEY3 = KEY2 ^ 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1

KEY123 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e ^ KEY3

FLAG = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf ^ KEY123

print(long_to_bytes(FLAG))
