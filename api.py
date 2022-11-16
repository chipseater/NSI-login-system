import json
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
@cross_origin()
def index():
    return jsonify({
        'text': 'Hello World',
    })


app.run(host='0.0.0.0', port=5000)
