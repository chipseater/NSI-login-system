from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller.todos import TodoManager
from middleware.token_required import token_required
from middleware.token_translater import encode, decode
from controller.auth import AuthManager
from dotenv import load_dotenv
from datetime import datetime


app = Flask(__name__)
load_dotenv()
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
@token_required
def index():
    TodoManager().createTable()
    return {
        'text': 'Hello World',
        'user_id': request.args.to_dict()['user_id'],
    }


@app.route('/add-todo', methods=['POST'])
@cross_origin()
@token_required
def addTodo():
    user_id = request.args.to_dict()['user_id']
    name = request.json['name']
    important = request.json['important']

    res = TodoManager().createTodo(user_id, name, important)

    return res


@app.route('/get-todos', methods=['GET'])
@cross_origin()
@token_required
def getUserTodos():
    user_id = request.args.to_dict()['user_id']

    res = TodoManager().getUserTodos(user_id)

    return res


@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    passwd = request.json['passwd']

    res = AuthManager().registerUser(first_name, last_name, email, passwd)
    if res['error']:
        return res
    
    access_token = encode(
        {'user_id': res['user_id']}, 'SECRET_KEY', lifespan=600)
    
    refresh_token = encode(
        {'user_id': res['user_id']},
        'REFRESH_KEY',
        lifespan=86400
    )

    AuthManager().storeRefreshToken(refresh_token)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.json['email']
    passwd = request.json['passwd']
    userVerification = AuthManager().verifyUser(email, passwd)

    if not userVerification['valid_passwd']:
        return {'error': 'Invalid credentials'}

    access_token = encode(
        {'user_id': userVerification['user_id']}, 'SECRET_KEY')
    
    refresh_token = encode(
        {'user_id': userVerification['user_id']},
        'REFRESH_KEY',
        lifespan=86400 # 1 day
    )

    AuthManager().storeRefreshToken(refresh_token)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@app.route('/get-token', methods=['POST'])
@cross_origin()
def get_token():
    refresh_token = request.json['refresh_token']
    res = AuthManager().isTokenInStorage(refresh_token)
    print(res)

    if not res['token_in_storage']:
        return {
            'error': 'Invalid refresh token'
        }

    data = decode(refresh_token, 'REFRESH_KEY')

    if 'error' in data:
        return data
    
    access_token = encode(data, 'SECRET_KEY')
    refresh_token = encode(data, 'REFRESH_KEY')

    AuthManager().storeRefreshToken(refresh_token)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }


@app.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    refresh_token = request.json['refresh_token']
    res = AuthManager().logout(refresh_token)

    if 'error' in res:
        return {
            'success': not res['error'],
            'error': res['error']
        }
    
    return {
        'error': 'Something bad happenened'
    }

app.run(host='0.0.0.0', port=5000, debug=True)
