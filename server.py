# TODO Aiming for the client to request or post not server send client stuff!
# ! Duplicated user_list[] utils.py and this file
import base64
import hashlib
import json
import os
import time
from socket import *

from fernet import Fernet

import chat_group
import utils
from utilities import password_check

s = socket()
user_list = []


class client:
    def __init__(self, socket_obj: object, auth=False, old_client=None):
        self.__client = socket_obj
        self.__old_client = old_client
        self.__auth = auth
        self.__username = 'Undefined'

    def login(self):
        key = Fernet.generate_key()
        if not self.__old_client is None:
            self.__client.sendall(json.dumps({'key': key.decode(), 'authed': self.__auth,
                                              'username': self.__old_client.get_nonsens_user_info()['username']}).encode())
        else:
            self.__client.sendall(json.dumps({'key': key.decode(), 'authed': self.__auth}).encode())

        if self.__auth:
            return None
        f = Fernet(key)
        login = self.__client.recv(4096)
        while not login:
            login = self.__client.recv(4096)
        login = f.decrypt(login).decode()
        login = json.loads(login)
        self.__username = login['username']
        result = password_check(login['username'], login['password'])
        if result == 200:
            self.__auth = True
            return chat_group.user(self.__username, utils.get_userid(self.__username), self.__client.getpeername()[0],
                                   self.__client, self.__auth, fernet_key=key)
        else:
            self.__client.sendall('401'.encode())
            logout(chat_group.user(self.__username, -1, None, self.__client, False, fernet_key=key), False)


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


def logout(usr, invalid=False):
    global user_list
    if invalid:
        os.remove(f"{os.getcwd()}/user_data/{usr.get_nonsens_user_info()['username']}.hash")
    usr.logout()
    print('Invalid login from:', usr.get_nonsens_user_info()['username'] + ", With user id:",
          usr.get_nonsens_user_info()['userid'])


def messaging(usr):
    while True:
        message = ''
        while not message:
            print(message)
            message = json.loads(usr.receive())
        print(message)

        username_list = [name.get_nonsens_user_info()['username'] for name in user_list]
        if message['to'] in username_list:
            to_id = username_list.index(message['to'])
            r_user = user_list[to_id]
            r_user.send(json.dumps(message))

        break

def get_connected_users(usr):
    global user_list
    usr.send(json.dumps({'Connected users': user_list}), encode=True)
    print('Sent connected users to', usr.get_nonsens_user_info()['address'])

def await_command(usr):
    command_dict = {'send_message': messaging, 'get_logged_users': get_connected_users}
    while True:
        data = usr.receive()
        command_dict.get(data)(usr)

if __name__ == '__main__':
    print('Starting server...')
    server_setup('127.0.0.1', 585)
    while True:
        c, addr = s.accept()
        print('Connection Received from:', addr, 'Accepting...')
        address_list = [name.get_nonsens_user_info()['address'] for name in user_list]
        c_ip = addr[0]
        if c_ip in address_list:
            usr_index = address_list.index(c_ip)
            authed_user = user_list[usr_index]
            authed_user.set_new_client_info(c, addr)
            client(c, True, authed_user).login()
        else:
            authed_user = client(c).login()

        if len(user_list) + 1 >= 10:
            authed_user.send('Server full!')
        else:
            if authed_user.get_nonsens_user_info()['username'] in [name.get_nonsens_user_info()['username'] for name in
                                                                   user_list] and not authed_user.get_auth():
                authed_user.send("\nCan't login with 2 sessions! / Username already taken!\n")
                logout(authed_user, invalid=True)

            else:
                if not authed_user.get_nonsens_user_info()['username'] in [name.get_nonsens_user_info()['username'] for
                                                                           name in user_list]:
                    user_list.append(authed_user)
                    authed_user.send(json.dumps(
                        {'connected_users': [name.get_nonsens_user_info()['username'] for name in user_list]}))
                    await_command(authed_user)
                else:
                    time.sleep(2)
                    await_command(authed_user)
                    
