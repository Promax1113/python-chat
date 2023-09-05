    # TODO Aiming for the client to request or post not server send client stuff!
from fernet import Fernet
from socket import *
import json
import chat_group, utils

s = socket()
user_list = []

class client:
    def __init__(self, socket_obj: object):
        self.__client = socket_obj
        self.__auth = False
        self.__username = 'Undefined'
    
    def login(self):
        key = Fernet.generate_key()
        self.__client.sendall(key)
        f = Fernet(key)
        login = self.__client.recv(4096)
        while not login:
            login = self.__client.recv(4096)
        login = f.decrypt(login).decode()
        login = json.loads(login)
        self.__username = login['username']
        # TODO Check if the password matches
        self.__auth = True
        return chat_group.user(self.__username, utils.get_userid(self.__username), self.__client.getsockname(), self.__client)
    


def server_setup(ip: str, port: int):
    address = (ip, port)
    global s
    s.bind(address)
    s.listen(5)

def logout(usr):
    global user_list
    usr._logout()
    print('Invalid login from:', usr.get_nonsens_user_info()['username'] + ", With user id:", usr.get_nonsens_user_info()['userid'])
    
    
if __name__ == '__main__':
    print('Starting server...')
    server_setup('', 585)

    while True:
        c, addr = s.accept()
        print('Connection Received from:', addr, 'Accepting...')
        address_list = [name.get_nonsens_user_info()['address'] for name in user_list]
        if addr in address_list:
            usr_index = address_list.index(addr)
            authed_user = user_list[usr_index]
            print(address_list, usr_index, user_list, user_list[usr_index].get_nonsens_user_info())
            
        
        authed_user = client(c).login()

        if len(user_list) + 1 >= 10:
            authed_user.send('Server full!')
        else:
            if authed_user.get_nonsens_user_info()['username'] in [name.get_nonsens_user_info()['username'] for name in user_list]:
                authed_user.send("\nCan't login with 2 sessions!\n")
                logout(authed_user)

            else:
                user_list.append(authed_user)
                authed_user.send(json.dumps({'connected_users': [name.get_nonsens_user_info()['username'] for name in user_list]}))
