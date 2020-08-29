from flask import Flask, jsonify, request
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

@app.route('/private', methods=['GET', 'POST'])
def getById():
    if request.method == 'POST':
        id = request.get_json().get('id')
        if(id == 1):
            return jsonify({'x': [1, 5, 3], 'y': [10, 20, 100]})
        else:
            return jsonify({'x': [1, 5, 8], 'y': [13, 28, 21], 'type': 'bar'})
    else: 
        return jsonify({'x': [1, 2, 3], 'y': [10, 20, 30]})


if __name__ == '__main__':
    app.run()