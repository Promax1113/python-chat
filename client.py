from socket import *
from fernet import Fernet
import json
from getpass import getpass
import time, hashlib, base64

client: object = socket()
tries: int = 0

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
        data = receive(client, 5)
        print(data)
        return None
    else:
        f = Fernet(data['key'].encode())
        send(socket=client, message=json.dumps({'username': input('Username: '), 'password': getpass()}), fernet=f, encode=False)
        data = receive(client, 10, f)
        print(data)
        try:
            print('Connected users', json.loads(data)['connected_users'])
        except:
            if data == '401':
                print('Unauthorised!')
            print(data)
    
if __name__ == '__main__':
    connect('127.0.0.1', 585)
    print('Connected to server!')
    login()

