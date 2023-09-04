import socket
import utils


s = socket.socket()


s.connect(('127.0.0.1', 5550))
message = s.recv(4096).decode()
key = s.recv(4096).decode()
print(key)
print('Bolas')
s.close()