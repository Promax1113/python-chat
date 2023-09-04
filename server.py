import json
import socket
from fernet import Fernet
import base64
import utils

key = Fernet.generate_key()

f = Fernet(key)

s = socket.socket()
s.bind(('127.0.0.1', 6969))

s.listen(5)
while True:
    
    #try:
    c, addr = s.accept()
    print('Connection from:', addr)
    c.sendall(key)
    print('sent')
    data = c.recv(4096)
    login = f.decrypt(data).decode()
    print(login)
    login_dict = json.loads(login)
    user = utils.login(login_dict['username'], login_dict['password'], addr)
    if user == 'Unauthorised!':
        c.sendall(('Unauthorised!').encode())
        c.close()
    else:
        c.sendall(('Access Granted!').encode())
    
    utils.menu(user, c)

    c.close()
    """except:
        c.sendall(('Server error!! Warn host about it it!').encode())
        c.close()"""