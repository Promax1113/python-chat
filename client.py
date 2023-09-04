import socket
from fernet import Fernet
import utils

key = Fernet(Fernet.generate_key())

s = socket.socket()

s.connect(('127.0.0.1', 6969))

user = utils.login()

s.send(str(user.get_nonsens_user_info()).replace("'", '"').encode())
s.close()