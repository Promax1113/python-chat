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

def receive(socket: object, timeout: float):
    data = ''
    start = time.time()
    while not data:
        time.sleep(1)
        data = socket.recvfrom(4096)
        message = data[0].decode()
        raddr = data[1]
        end = time.time()
        if round(end - start) >= timeout:
            print('Timeout exceeded for data tranfer!')
            exit(1)
    return {'raddr': raddr, 'data': message}
def send(socket: object):
    # TODO Add encryption to comunication
    pass

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
    data = receive(client, 10)['data']
    print(data)
    data = json.loads(data)
    if data['authed'] == True:
        print(f"Logged in as {data['username']}")
        data = receive(client, 3)['data']
        print(data)
        return None
    else:
        f = Fernet(data['key'].encode())
        token = f.encrypt(json.dumps({'username': input('Username: '), 'password': getpass()}))
        client.sendall(token)
        data = receive(client, 10)['data']
        try:
            print('Connected users', json.loads(data)['connected_users'])
        except:
            print(data)
    
if __name__ == '__main__':
    connect('127.0.0.1', 585)
    print('Connected to server!')
    login()

