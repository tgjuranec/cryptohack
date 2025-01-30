import pwn
import json
from Crypto.Util.number import long_to_bytes
a = {'buy': 'flag'}
request = json.dumps(a)

HOST = "socket.cryptohack.org"
PORT = 13377
conn = pwn.remote(HOST,PORT)
response = conn.recv(2400).decode()
print(response)
injson = json.loads(response)
injson
conn.close()
#conn.send(request.encode())
#response = conn.recvline().decode()
#print(response)