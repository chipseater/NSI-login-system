import jwt
import os

def encode(dict):
    return jwt.encode(dict, os.getenv('SECRET_KEY'))
