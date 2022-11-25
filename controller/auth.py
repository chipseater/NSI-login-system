from .dbFunc import dbFunc
import sqlite3
import os
import hashlib


class AuthManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/auth.db')

    @staticmethod
    def hashPasswd(passwd, passwd_salt):
        passwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            passwd.encode('utf-8'),
            passwd_salt,
            100000
        ).hex()

        return passwd_hash + passwd_salt.hex()


    @dbFunc
    def resetDatabase(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY,
            first_name varchar(255),
            last_name varchar(255),
            email varchar(255) NOT NULL,
            passwd_hash varchar(255)
        ) """)

    @dbFunc
    def registerUser(self, cursor, first_name, last_name, email, passwd):
        passwd_hash = AuthManager.hashPasswd(passwd, os.urandom(32))

        cursor.execute(f"""
            INSERT INTO users (first_name, last_name, email, passwd_hash) VALUES (
                "{first_name}", "{last_name}", "{email}", "{passwd_hash}"
            )
        """)

    @dbFunc
    def verifyUser(self, cursor, email, passwd):
        payload = cursor.execute(f"""
            SELECT passwd_hash, id FROM users WHERE email = "{email}"
        """).fetchone()

        if not payload:
            return {
                "valid_passwd": False,
                "user_id": -1,
                "error": f"No user with email {email}",
            }

        passwd_hash_from_db, user_id = payload
        print(passwd_hash_from_db, user_id)

        passwd_key_from_db = passwd_hash_from_db[:64]
        passwd_salt_from_db = bytes.fromhex(passwd_hash_from_db[64:])

        passwd_hash_from_request = AuthManager.hashPasswd(passwd, passwd_salt_from_db)

        return {
            "valid_passwd": passwd_hash_from_db == passwd_hash_from_request,
            "user_id": user_id,
        }        


if __name__ == '__main__':
    if input('Do you really want to wipe out all of the user data ?') == 'y':
        authmanager = AuthManager()
        authmanager.resetDatabase()
