from socket import *
from fernet import Fernet
import json
from getpass import getpass
import time

client: object = socket()
tries: int = 0

# TODO make it configurable!
def connect(ip: str, port: int):
    global client, tries
    try:
        client.connect((ip, port))
    except:
        if tries <= 5:
            print('Host possibly offline, now retrying...')
            tries += 1
            time.sleep(1.0)
            connect(ip, port)
            
        else:
            print('Retried 5 times, no response. Quitting...')
            exit(1)
def login():
    data = ''
    while not data:
        data = client.recv(4096)
    f = Fernet(data)
    token = f.encrypt(json.dumps({'username': input('Username: '), 'password': getpass()}))
    client.sendall(token)
    data = ''
    while not data:
        data = client.recv(4096).decode()
    try:
        print('Connected users', json.loads(data)['connected_users'])
    except:
        print(data)
    
if __name__ == '__main__':
    connect('192.168.1.50', 585)
    print('Connected to server!')
    login()

