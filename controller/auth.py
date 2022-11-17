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
            name text NOT NULL,
            begin_date text,
            end_date text
        ); """)


authmanager = AuthManager()
authmanager.helloWorld()
