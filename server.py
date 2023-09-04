import json
import socket

s = socket.socket()
print((socket.gethostname(), 6969))
s.bind(('127.0.0.1', 6969))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Connection from:', addr)
    c.send(('Connected to server!!').encode())
    message = c.recv(4096).decode()

    message = json.loads(message)
    print(message)

    c.close()