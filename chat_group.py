import hashlib

group_list = []


class _group:
    def __init__(self, name: str, author: str, group_hash: str):
        self.name = name
        self.__author = author
        self.__hash = group_hash
        self.user_list = []
        self.__join_message = f'Welcome to {self.name}!'
    
    def set_join_message(self, message: str):
        self.__join_message = message
    def get_join_message(self):
        return self.__join_message
    def get_hash(self):
        return self.__hash
    
    def get_info(self):
        return {'name': self.name, 'author': self.__author, 'user_list': self.user_list, 'join_message': self.__join_message}

class user:
    def __init__(self, username: str, userid: int, address: str):
        self.__username = username
        self.__userid = userid
        self.__owned_groups = []
        self.__joined_groups = []
        self.address: str

    def create_group(self, name: str, password: str):
        __group_hash = hashlib.sha256(f'{name}{password}'.encode('utf-8')).hexdigest()
        group_chat = _group(name, self.__username, __group_hash)
        self.__owned_groups.append({'name': group_chat.name, 'obj': group_chat})
        self.__joined_groups.append({'name': group_chat.name, 'obj': group_chat})
        group_list.append({'name': group_chat.name, 'obj': group_chat})
        return group_chat.name

    def join_group(self, name: str, password: str):
        chat_to_join = 'undefined'
        for chat in group_list:
            if name == chat['name']:
                chat_to_join = chat['obj']
        if chat_to_join == 'undefined':
            print('Group not found!')
            exit(1)
            # TODO Return to menu
        if hashlib.sha256(f'{name}{password}'.encode('utf-8')).hexdigest() == chat_to_join.get_hash():
            self.__joined_groups.append([chat_to_join.name, {'obj': chat_to_join}])
            print('Joined', chat_to_join.name)
            chat_to_join.user_list.append(self.__username)
            print(f'Message: {chat_to_join.get_join_message()}')
        else:
            print('Incorrect password!!')


    def get_nonsens_user_info(self):
        return {"username": self.__username, "userid": self.__userid, "owned_groups": self.__owned_groups, "joined_groups": self.__joined_groups}
