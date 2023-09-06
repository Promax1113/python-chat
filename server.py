    # TODO Aiming for the client to request or post not server send client stuff!
    # ! Duplicated user_list[] utils.py and this file
from fernet import Fernet
from socket import *
import json
import chat_group, utils
from security_utils import password_check
import os, time, hashlib, base64

s = socket()
user_list = []

class client:
    def __init__(self, socket_obj: object, auth = False, old_client = None):
        self.__client = socket_obj
        self.__old_client = old_client
        self.__auth = auth
        self.__username = 'Undefined'
    
    def login(self):
        key = Fernet.generate_key()
        if not self.__old_client == None:
            self.__client.sendall(json.dumps({'key': key.decode(), 'authed': self.__auth, 'username': self.__old_client.get_nonsens_user_info()['username']}).encode())
        else:
            self.__client.sendall(json.dumps({'key': key.decode(), 'authed': self.__auth}).encode())

        if self.__auth == True:
            
            return None
        f = Fernet(key)
        login = self.__client.recv(4096)
        while not login:
            login = self.__client.recv(4096)
        login = f.decrypt(login).decode()
        login = json.loads(login)
        self.__username = login['username']
        password_check(login['username'], login['password'])
        self.__auth = True
        return chat_group.user(self.__username, utils.get_userid(self.__username), self.__client.getpeername()[0], self.__client, self.__auth)
    
def gen_fernet_key(passcode: bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def server_setup(ip: str, port: int):
    address = (ip, port)
    global s
    s.bind(address)
    s.listen(5)

def logout(usr, invalid = False):
    global user_list
    if invalid:
        os.remove(f"{os.getcwd()}/user_data/{usr.get_nonsens_user_info()['username']}.hash")
    usr._logout()
    print('Invalid login from:', usr.get_nonsens_user_info()['username'] + ", With user id:", usr.get_nonsens_user_info()['userid'])
    
    
if __name__ == '__main__':
    print('Starting server...')
    server_setup('127.0.0.1', 585)

    while True:
        c, addr = s.accept()
        print('Connection Received from:', addr, 'Accepting...')
        address_list = [name.get_nonsens_user_info()['address'] for name in user_list]
        ip = addr[0]
        if ip in address_list:
            usr_index = address_list.index(ip)
            authed_user = user_list[usr_index]
            authed_user.set_new_socket(c)
            client(c, True, authed_user).login()
        else:
            authed_user = client(c).login()
        
        if len(user_list) + 1 >= 10:
            authed_user.send('Server full!')
        else:
            if authed_user.get_nonsens_user_info()['username'] in [name.get_nonsens_user_info()['username'] for name in user_list] and not authed_user.get_auth():
                authed_user.send("\nCan't login with 2 sessions! / Username already taken!\n")
                logout(authed_user, invalid=True)
            
            else:
                if not authed_user.get_nonsens_user_info()['username'] in [name.get_nonsens_user_info()['username'] for name in user_list]:
                    user_list.append(authed_user)
                    authed_user.send(json.dumps({'connected_users': [name.get_nonsens_user_info()['username'] for name in user_list]}))
                else:
                    print('bALLS')
                    time.sleep(2)
                    authed_user.send(f"Hello! {authed_user.get_nonsens_user_info()['username']}")