import json, os

from sqlitedict import SqliteDict

db = SqliteDict(f'{os.getcwd()}/../server.db', outer_stack=False)


def write_database(to_write: dict) -> None:
    f_to_write = json.dumps(to_write)
    if len(db) == 0:
        last_index = 0
    else:
        last_index = (len(db) - 1)
    print(last_index)
    db[last_index] = f_to_write
    db.commit()


def read_database():
    global db
    user: list = []
    for key, item in db.items():
        user.append(json.loads(item))
    return user

print(read_database())