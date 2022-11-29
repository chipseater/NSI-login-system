from werkzeug.datastructures import ImmutableMultiDict
from flask import request
from .token_translater import decode


def token_required(func):
    def inner(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return {'error': 'a valid token is missing'}

        data = decode(token, 'SECRET_KEY')

        if 'error' in data:
            return {'error': 'Expired token'}

        http_args = request.args.to_dict()
        http_args['user_id'] = data['user_id']

        request.args = ImmutableMultiDict(http_args)

        return func(*args, **kwargs)
    return inner
