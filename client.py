import socket
from getpass import getpass
from fernet import Fernet
import json





s = socket.socket()
ip = '127.0.0.1'
port = 6969

try:
    s.connect((ip, port))
except:
    print("Connection refused or host not online!")
    exit(1)
try:
    key = s.recv(4069)
    f = Fernet(key)
    username, password = input('Username: '), getpass() 
    to_encrypt = json.dumps({"username": username, "password": password})
    token = f.encrypt((to_encrypt.encode()))
    s.sendall(token)
    print("\n" + s.recv(4096).decode() + "\n")
    print(s.recv(4096).decode())
    s.sendall(input('Choice: ').encode())
    print("Your info: " + s.recv(4096).decode())
except:
    print('Error occurred while running code! Exiting...')
    exit(1)