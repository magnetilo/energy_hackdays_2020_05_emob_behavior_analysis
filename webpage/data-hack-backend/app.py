from flask import Flask, jsonify
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def test_fct():
    return {'x': [1, 2, 3], 'y': [10, 20, 30], 'type': 'bar'}

@app.route('/', methods=['GET'])
def index():
    return jsonify(test_fct())

@app.route('/private', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()