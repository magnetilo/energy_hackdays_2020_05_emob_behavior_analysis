from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Create path to the project
app_file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(app_file_path, '..', '..'))
# Add project path to the PYTHONPATH system variable
sys.path.append(os.path.abspath(project_path))
# Import private data set functions
from src_private.load_process import load_private, data_preprocess
# Load an preprocess the data
df = data_preprocess(load_private("../../private_data/metervalues_anonymized.csv"))

def get_private_ids(df):
    """Get all the unique connectors"""
    return df['chargepoint_connector'].unique().tolist()
def test_plots(df, id):
    """Test function"""
    sub_df = df[df['chargepoint_connector'] == id]
    return [{
        'x': sub_df['timestamp'].values.tolist(),
        'y': sub_df['increment'].tolist(),
        'mode': 'lines',
        'type': 'scatter',
        'name': 'plot_1'
    },
    {
        'x': sub_df['timestamp'].values.tolist(),
        'y': (sub_df['increment'] + 1000).tolist(),
        'mode': 'lines',
        'type': 'scatter',
        'name': 'plot_2'
    }
    ]


def test_fct():
    return [{'y': [
    0.01896241171045365576 * 100, 
    0.05943275750876332473 * 100,
    0.04244929596970110481 * 100,
    0.02563388334773649259 * 100,
    0.02294805453940804789 * 100,
    0.04810573870890297678 * 100,
    0.04712317096368065783 * 100,
    0.06464654698386771179 * 100,
    0.05660705272141365258 * 100], 
    'x': [
        'Agrargemeinden',
        'Grosszentren',
        'Gürtel der Grosszentren',
        'Gürtel der Mittelzentren',
        'Kleinzentren',
        'Mittelzentren',
        'Nebenzentren der Grosszentren',
        'Periurbane ländliche Gemeinden',
        'Touristische Gemeinden'
    ], 'type': 'bar'}]

@app.route('/', methods=['GET'])
def index():
    return jsonify(test_fct())

@app.route('/private', methods=['GET', 'POST'])
def getById():
    if request.method == 'POST':
        id = request.get_json().get('id')
        return json.dumps(test_plots(df, id))
    else: 
        return json.dumps(get_private_ids(df))


if __name__ == '__main__':
    app.run()