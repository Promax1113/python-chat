import base64
import os
import chat_group
from getpass import getpass
import hashlib


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


def login():
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
        return chat_group.user(username, get_userid(username))
    else:
        print('Access Denied!')
        login()

def menu(usr):
    if input('1 for creating group, 2 for joining one') == '1':
        usr.create_group(input('Name: '), getpass())
    elif input('1 for creating group, 2 for joining one') == '2':
        usr.join_group(input('Name: '), getpass())