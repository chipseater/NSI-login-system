from werkzeug.datastructures import ImmutableMultiDict
from dotenv import dotenv_values
from flask import request


def token_required(func):
    def inner(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'error': 'a valid token is missing'})

        try:
            data = jwt.decode(
                token, config('SECRET_KEY'), algorithms=["HS256"]
            )

            http_args = request.args.to_dict()
            http_args['user_id'] = data.id

            request.args = ImmutableMultiDict(http_args)
        except:
            return jsonify({'error': 'token is invalid'})

        return func(*args, **kwargs)
    return inner
