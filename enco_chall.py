from pwn import * # pip install pwntools
import json
from Crypto.Util.number import *

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


while True:

    received = json_recv()
    decoded = ""
    try:
        enctype = received['type']
        if enctype == None:
            print("Received flag: ", received['flag'])
            break
        if enctype == "base64":
            decoded = b64d(received['encoded']).decode()
        elif enctype == "hex":
            decoded = bytes.fromhex(received['encoded']).decode()
        elif enctype == "rot13":
            for c in received['encoded']:
                if c.islower():
                    decoded += chr((ord(c)-ord('a')+13)%26 + ord('a'))
                elif c.isupper():
                    decoded += chr((ord(c)-ord('A')+13)%26 + ord('A'))
                else:
                    decoded += c
        elif enctype == "bigint":
            decoded = long_to_bytes(int(received['encoded'], 16)).decode()
        elif enctype == "utf-8":
            decoded = ''.join([chr(i) for i in received['encoded']])
        else:   
            print("Unknown encoding")
            break
        to_send = {
            "decoded": decoded
        }
        json_send(to_send)
    except:
        print("Failed to decode")
        break
received = json_recv()






json_send(to_send)

json_recv()
