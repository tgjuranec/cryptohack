from pwn import *

x = 0x6865617465645f72756e6e696e675f61637475616c6c79


def hex_to_ascii(hex_str):
    return bytes.fromhex(hex_str).decode()

print(hex_to_ascii(hex(x)[2:]))