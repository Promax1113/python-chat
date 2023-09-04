import socket
from getpass import getpass
from fernet import Fernet





s = socket.socket()

try:
    s.connect(('127.0.0.1', 6969))
except:
    print("Connection refused or host not online!")
    exit(1)
try:
    key = s.recv(4069)
    f = Fernet(key)
    username, password = input('Username: '), getpass() 
    to_encrypt = '{"username": ' + username + ', "password": ' + password + "}"
    token = f.encrypt((to_encrypt.encode()))
    s.sendall(token)
    print("\n" + s.recv(4096).decode())
    
    s.close()
except:
    print('Error occurred while running code! Exiting...')
    exit(1)