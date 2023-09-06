import hashlib, os
def folder_check(username):
    userpath = os.getcwd()
    filepath = f'{userpath}/user_info/{username}.hash'
    
    if not os.path.isdir(f'{userpath}/user_info'):
        os.mkdir(f'{userpath}/user_info/')
    if not os.path.isfile(filepath):
        with open(filepath, 'w+') as f:
            f.close()
        return None
    else:
        with open(filepath, 'r+') as f:
            return f.readline()


def save_password(hash, username):   
    #TODO Save Password! 
    pass

def password_check(username, password):
    hashed_pass = hashlib.sha256((username + password).encode())
    hashfile_data = folder_check(username)
    if not hashfile_data:
        print('Saving pasword as it is the first time!')
        # TODO call password saver!
    else:
        if hashed_pass == hashfile_data: return 200 
        else: return 401
    
print(password_check('balls', 'baller'))