import datetime
import time
import jwt
import os


def encode(dict, key, lifespan=600):
    if lifespan > 0:
        dict["exp"] = time.mktime(
            (datetime.datetime.now() + datetime.timedelta(seconds=lifespan)).timetuple()
        )
    return jwt.encode(dict, os.getenv(key))


def decode(token, key):
    try:
        return jwt.decode(
            token, os.getenv(key), algorithms=["HS256"]
        )
    except jwt.exceptions.ExpiredSignatureError:
        return {'error': 'Token expired'}
