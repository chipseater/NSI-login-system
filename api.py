import controller.auth as authCtl
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
@cross_origin()
def index():
    return {
        'text': 'Hello World',
    }


@app.route('/register', methods=["POST"])
@cross_origin()
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    passwd = request.json['passwd']
    return authCtl.AuthManager().registerUser(first_name, last_name, email, passwd)


@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    email = request.json['email']
    passwd = request.json['passwd']
    return authCtl.AuthManager().verifyUser(email, passwd)


app.run(host='0.0.0.0', port=5000, debug=True)
