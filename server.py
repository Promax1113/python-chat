import json
import socket
from fernet import Fernet
import base64
import utils

key = utils.gen_fernet_key((f'handshake-{base64.encodebytes(socket.gethostname().encode())}').encode())

f = Fernet(key)

s = socket.socket()
print((socket.gethostname(), 6969))
s.bind(('127.0.0.1', 2133))

s.listen(5)
print(key)
while True:
    c, addr = s.accept()
    print('Connection from:', addr)
    c.send(bytes("200", 'utf-8'))
    c.send(str(key).encode())
    print('bolas')
    login = c.recv(4096).decode()
    json.loads(login)

    message = json.loads(message)
    print(message)

    c.close()