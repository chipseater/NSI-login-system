import datetime
import time
import jwt
import os


def encode(dict, key):
    dict["exp"] = time.mktime(
        (datetime.datetime.now() + datetime.timedelta(seconds=30)).timetuple()
    )
    return jwt.encode(dict, os.getenv(key))
