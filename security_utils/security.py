import hashlib, os
def folder_check(username: str):
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
            data = f.readline()
            f.close()
            return data


def save_password(hash: str, username: str):   
    userpath = os.getcwd()
    filepath = f'{userpath}/user_info/{username}.hash'
    with open(filepath, 'w+') as f:
        f.write(hash)
        f.close()

def password_check(username: str, password: str):
    hashed_pass = hashlib.sha256((username + password).encode()).hexdigest()
    hashfile_data = folder_check(username)
    if not hashfile_data:
        print('Saving pasword as it is the first time!')
        save_password(hashed_pass, username)
        print('Success!')
        return 200
    else:
        if hashed_pass == hashfile_data: 
            print('Success!')
            return 200 
        else:
            print('Unauthorised!') 
            return 401