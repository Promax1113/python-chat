from socket import *
from fernet import Fernet
import json
from getpass import getpass
import time, hashlib, base64

client: object = socket()
tries: int = 0
sent_messages = []

class message:
    def __init__(self, author: str, recipient: str, content: str) -> None:
        self.__from_username = author
        self.__to_username = recipient
        self.__content = content

    def get_data(self) -> dict:
        return {'from': self.__from_username, 'to': self.__to_username, 'content': self.__content}


def gen_fernet_key(passcode: bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


def receive(socket: object, timeout: float, fernet: object = None):
    data = ''
    start = time.time()
    while not data:
        time.sleep(1)
        data = socket.recv(4096)
        if not fernet:
            data = data.decode()
        else:
            data = fernet.decrypt(data).decode()
        end = time.time()
        if round(end - start) >= timeout:
            print('Timeout exceeded for data tranfer!')
            exit(1)
        return data
def send(socket: object, message: str, fernet: object = None, encode: bool = True):
    # TODO Add encryption to comunication
    if encode:
        if not fernet:
            socket.sendall(message.encode())
        else:
            socket.sendall(fernet.encrypt(message.encode()))
    else:
        if not fernet:
            socket.sendall(message)
        else:
            socket.sendall(fernet.encrypt(message))

# TODO make it configurable!
def connect(ip: str, port: int):
    global client, tries
    try:
        client.connect((ip, port))
    except:
        if tries <= 5:
            print('Host possibly offline, now retrying...')
            tries += 1
            time.sleep(2)
            connect(ip, port)
            
        else:
            print('Retried 5 times, no response. Quitting...')
            exit(1)
def login():
    data = receive(client, 10)
    data = json.loads(data)
    if data['authed'] == True:
        print(f"Logged in as {data['username']}")
        _data = receive(client, 5)
        print(_data)
        return data
    else:
        f = Fernet(data['key'].encode())
        user_info = {'username': input('Username: '), 'password': getpass()}
        login_data = json.dumps(user_info)
        send(socket=client, message=login_data, fernet=f, encode=False)
        data = receive(client, 10, f)
        try:
            print('Connected users', json.loads(data)['connected_users'])
        except:
            if data == '401':
                print('Unauthorised!')
                client.close()
            print(data, 'balls')
            return {'username': 'Undefined', 'key': f}
        return {'username': user_info['username'], 'key': f}
def messaging(key):
    global username
    msg = message(username, input('Username of the recipient (case sensitive): '), input('Message to send: '))
    sent_messages.append(msg)
    print(msg.get_data())
    if input('Send? (y/N): ').lower() == 'y':
        send(client, json.dumps(msg.get_data()), key, True)
    data = ''
    while not data:
        data = receive(client, 10, key)
    data = json.loads(data)
    print(f"Message from {data['from']}. Message: {data['content']}")
if __name__ == '__main__':
    connect('127.0.0.1', 585)
    print('Connected to server!')
    result = login()
    print(result)
    fernet_obj = result['key']
    username = result['username']
    print(fernet_obj)
    messaging(fernet_obj)

