from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from middleware.token_required import token_required
from middleware.tokenTranslater import encode, decode
from controller.auth import AuthManager
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
@token_required
def index():
    return {
        'text': 'Hello World',
        'user_id': request.args.to_dict()['user_id'],
    }


@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    passwd = request.json['passwd']
    return AuthManager().registerUser(first_name, last_name, email, passwd)


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
        'REFRESH_KEY'
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

    return {
        'access_token': encode(data, 'SECRET_KEY')
    }


app.run(host='0.0.0.0', port=5000, debug=True)
