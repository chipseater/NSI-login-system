from .db_func import db_func
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

    @db_func
    def resetDatabase(self, cursor):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id integer PRIMARY KEY,
            token varchar(255)
        ) """)

    @db_func
    def registerUser(self, cursor, first_name, last_name, email, passwd):
        passwd_hash = AuthManager.hashPasswd(passwd, os.urandom(32))

        cursor.execute(f"""
            INSERT INTO users (first_name, last_name, email, passwd_hash) VALUES (
                "{first_name}", "{last_name}", "{email}", "{passwd_hash}"
            )
        """)

        res = cursor.execute(f"""
            SELECT id FROM users WHERE email = "{email}"
        """).fetchone()

        return {
            'user_id': res[0]
        }


    @db_func
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
        passwd_salt_from_db = bytes.fromhex(passwd_hash_from_db[64:])
        passwd_hash_from_request = AuthManager.hashPasswd(
            passwd, passwd_salt_from_db)

        return {
            "valid_passwd": passwd_hash_from_db == passwd_hash_from_request,
            "user_id": user_id,
        }

    @db_func
    def storeRefreshToken(self, cursor, token):
        cursor.execute(f"""INSERT INTO refresh_tokens (token) VALUES (
            "{token}"
        )"""
    )

    @db_func
    def isTokenInStorage(self, cursor, token):
        res = cursor.execute(
            f"""
                SELECT id FROM refresh_tokens WHERE token = "{token}"
            """
        ).fetchone()

        if res:
            return {'token_in_storage': True}
        return {'token_in_storage': False}

    @db_func
    def logout(self, cursor, refresh_token):
        cursor.execute(f"""
            DELETE FROM refresh_tokens WHERE token = "{refresh_token}"
        """)
