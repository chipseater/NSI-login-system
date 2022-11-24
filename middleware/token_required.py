from werkzeug.datastructures import ImmutableMultiDict
from dotenv import dotenv_values
from flask import request
import jwt
import os


def token_required(func):
    def inner(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            print(token)

        if not token:
            return {'error': 'a valid token is missing'}


        data = jwt.decode(
            token, os.getenv('SECRET_KEY'), algorithms=["HS256"]
        )

        http_args = request.args.to_dict()
        http_args['user_id'] = data.id

        request.args = ImmutableMultiDict(http_args)

        return func(*args, **kwargs)
    return inner
