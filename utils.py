import base64
import os
import chat_group
from getpass import getpass
import hashlib
import json



# TODO Add to server when networking!
user_list = []

def gen_fernet_key(passcode: bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


class get_group_info:

    def by_name(self, user_obj, name):
        for group in user_obj.get_nonsens_user_info()['joined_groups']:
            if group['name'] == name:
                return group['obj']


get_info_group = get_group_info()


def get_userid(__username):
    user_list.append(__username)
    userid = (user_list.index(__username) + 1)
    user_list.append(userid)
    user_list.pop(userid)
    return userid


def login(username = None, password = None, ip_address = None):
    if username == None and password == None:       
        username = input('Username: ')
        password = getpass()
        pass_hash: str = hashlib.sha256((username+password).encode()).hexdigest()
        if not os.path.isfile('pass.hash'):
            with open('pass.hash', 'w') as f:
                f.write(pass_hash)
                f.close()
            pass_file = pass_hash
        else:
            with open('pass.hash', 'r') as f:
                pass_file = f.readline()
        if pass_hash == pass_file:
            print('Access granted!')
            return chat_group.user(username, get_userid(username), ip_address)
        else:
            print('Access Denied!')
            login()
    else:
        pass_hash: str = hashlib.sha256(bytes(f"{username}{password}", 'utf-8')).hexdigest()
        userid = get_userid(username)
        if not os.path.isfile(f'{username}.hash'):
            with open(f'{username}.hash', 'w') as f:
                f.write(pass_hash)
                f.close()
            pass_file = pass_hash
        else:
            with open(f'{username}.hash', 'r') as f:
                pass_file = f.readline()
        if pass_hash == pass_file:
            print('Access granted!')
            return chat_group.user(username, userid, ip_address)
        else:
            print('Access Denied for', username)
            return 'Unauthorised!'   
    

def menu(usr, C_socket = None, fernet_key = None):
    if C_socket == None:
        choice = input('1 for creating group, 2 for joining one 3 for viewing info')
        if choice == '1':
            usr.create_group(input('Name: '), getpass())
        elif choice == '2':
            usr.join_group(input('Name: '), getpass())
        elif choice == "3":
            usr.get_nonsens_user_info()
    else:
        C_socket.sendall(('1 for creating group, 2 for joining one 3 for viewing info:').encode())
        response = C_socket.recv(4096).decode()
        if response == '1':
            C_socket.sendall(usr.create_group(input('Name: '), getpass()))
        elif response == '2':
            C_socket.sendall(usr.join_group(input('Name: '), getpass()))
        elif response == "3":
            print(fernet_key.encrypt(json.dumps(usr.get_nonsens_user_info()).encode()))
            C_socket.sendall(fernet_key.encrypt(json.dumps(usr.get_nonsens_user_info()).encode()))
        else:
            return 'Invalid'