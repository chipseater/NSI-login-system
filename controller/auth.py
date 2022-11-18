import sqlite3, os, hashlib


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
    def resetDatabase(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY,
            first_name varchar(255),
            last_name varchar(255),
            email varchar(255) NOT NULL,
            passwd_hash varchar(255)
        ); """)

    @dbFunc
    def registerUser(self, cursor, first_name, last_name, email, passwd):
        passwd_salt = os.urandom(32)
        passwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            passwd.encode('utf-8'),
            passwd_salt,
            100000
        ).hex()

        cursor.execute(f"""
            INSERT INTO users (first_name, last_name, email, passwd_hash) VALUES (
                "{first_name}", "{last_name}", "{email}", "{passwd_hash + passwd_salt.hex()}"
            )
        """)


if __name__ == '__main__':
    if input('Do you really want to wipe out all of the user data ?') == 'y':
        authmanager = AuthManager()
        authmanager.resetDatabase()
