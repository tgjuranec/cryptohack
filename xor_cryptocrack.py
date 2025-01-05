from Crypto.Util.number import *


def xor(text, key):
    ret = b''
    for b in text:
        ret += (b ^key).to_bytes(1, 'big')
    return ret


s = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
bCrypto = b'myXORkey'
mEnc = bytes.fromhex(s)
bKey = b''
for i in range(len(mEnc)):
    bKey += bytes([bCrypto[i%len(bCrypto)] ^ mEnc[i]])

print(bKey)


