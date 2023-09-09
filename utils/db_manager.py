import json
from test import read_database

from sqlitedict import SqliteDict

db = SqliteDict('server.db', outer_stack=False)


def write_database(to_write: dict) -> None:
    f_to_write = json.dumps(to_write)
    last_index = (len(read_database()) - 1)
    print(last_index)
    db[last_index] = f_to_write
    db.commit()
    db.close()


write_database({"message": 'hello'})
write_database({"message": '23'})
write_database({"message": 'grhr'})
