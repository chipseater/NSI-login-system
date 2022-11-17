import sqlite3


def dbFunc(func):
    def inner(self, *args, **kwargs):
        cursor = self.conn.cursor()
        func(self, cursor, *args, **kwargs)
        self.conn.commit()
    return inner


class AuthManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/auth.db')
    

    @dbFunc
    def helloWorld(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY,
            first_name varchar(255),
            last_name varchar(255),
            email varchar(255) NOT NULL,
            passwd_hash varchar(255),
            passwd_salt varchar(255)
        ); """)


authmanager = AuthManager()
authmanager.helloWorld()
