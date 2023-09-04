import random
import os
import chat_group
import string
import hashlib


class get_group_info:

    def by_name(self, user_obj, name):
        for group in user_obj.get_nonsens_user_info()['joined_groups']:
            if group['name'] == name:
                return group['obj']


get_info_group = get_group_info()


def get_userid(__username):
    global user_list
    user_list.append(__username)
    userid = (user_list.index(__username) + 1)
    user_list.append(userid)
    user_list.pop(userid)
    return userid


def login():
    username = input('Username: ')
    password = input('Password: ')
    pass_hash: str = hashlib.sha256((username+password).encode()).hexdigest()
    if not os.listdir('pass.hash'):
        with open('pass.hash', 'w') as f:
            f.write(pass_hash)
            f.close()
    else:
        with open('pass.hash', 'r') as f:
            pass_file = f.readline()
    if pass_hash == pass_file:
        print('Access granted!')
        return chat_group.user(username, get_userid(username))
    else:
        print('Access Denied!')
        login()

