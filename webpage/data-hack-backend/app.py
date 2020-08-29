from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import json
import pandas as pd

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
from src_private.population_plot import load_curve, overall_load_curve_plt, median_load_energy_plt, charging_amount, charging_amount_plt, total_consumption, total_consumption_plt, plot_hourly_consumption, charge_type_v_cid
from src_private.user_plot import plot_consumption_history, plot_charging_history, plot_distribution_charging_begin_day, plot_distribution_charging_begin_hour, plot_charging_time_distribution, plot_distribution_programmed_charging, plot_energy_by_charge_distribution, plot_percentage_maxcharge, plot_monthly_cost

# Load an preprocess the data
df = data_preprocess(load_private("../../private_data/metervalues_anonymized.csv"))

list_filter = ['is_extrem_value', 'is_charging', 'is_too_long_charging']
df_clean = df[(df['is_extrem_value'] == False) & (df['is_charging'] == True) & (df['is_too_long_charging'] == False)]
load_curve_df = load_curve(df_clean)

def hour_profile():
    df_total = pd.DataFrame()
    with open('../../public_temporal_data/hour_profile_per_region_per_weektime.json') as f:
        df = pd.read_json(f)
        df = df.transpose()
        city_center = df[df['region'] == 'city centers']
        city_center_weekdays = city_center[city_center['weektime'] == 'weekday']
        x1 = city_center_weekdays['hour'].tolist()
        y1 = (city_center_weekdays['occupied_ratio']*100).tolist()
        title1 = 'City Center Weekday'

        country_side = df[df['region'] == 'country side']
        country_side_weekdays = country_side[country_side['weektime'] == 'weekday']
        x2 = country_side_weekdays['hour'].tolist()
        y2 = (country_side_weekdays['occupied_ratio']*100).tolist()
        title2 = 'Country Side Weekday'

        touristic = df[df['region'] == 'touristic']
        touristic_weekdays = touristic[touristic['weektime'] == 'weekday']
        x3 = touristic_weekdays['hour'].tolist()
        y3 = (touristic_weekdays['occupied_ratio']*100).tolist()
        title3 = 'Touristic Weekday'

    return [
        {'type': 'bar','name': title1,
        'x': x1,
        'y': y1},
        {'type': 'bar','name': title2,
        'x': x2,
        'y': y2},
        {'type': 'bar','name': title3,
        'x': x3,
        'y': y3}
    ]

def hour_profile_WE():
    df_total = pd.DataFrame()
    with open('../../public_temporal_data/hour_profile_per_region_per_weektime.json') as f:
        df = pd.read_json(f)
        df = df.transpose()
        city_center = df[df['region'] == 'city centers']
        city_center_weekend = city_center[city_center['weektime'] == 'weekend']
        x1 = city_center_weekend['hour'].tolist()
        y1 = (city_center_weekend['occupied_ratio']*100).tolist()
        title1 = 'City Center Weekend'

        country_side = df[df['region'] == 'country side']
        country_side_weekend = country_side[country_side['weektime'] == 'weekend']
        x2 = country_side_weekend['hour'].tolist()
        y2 = (country_side_weekend['occupied_ratio']*100).tolist()
        title2 = 'Country Side Weekend'

        touristic = df[df['region'] == 'touristic']
        touristic_weekend = touristic[touristic['weektime'] == 'weekend']
        x3 = touristic_weekend['hour'].tolist()
        y3 = (touristic_weekend['occupied_ratio']*100).tolist()
        title3 = 'Touristic Weekend'

    return [
        {'type': 'bar','name': title1,
        'x': x1,
        'y': y1},
        {'type': 'bar','name': title2,
        'x': x2,
        'y': y2},
        {'type': 'bar','name': title3,
        'x': x3,
        'y': y3}
    ]

def lat_lon():
    df_total = pd.DataFrame()
    with open('../../public_temporal_data/occupied_ratio_per_lat_lng.json') as f:
        df = pd.read_json(f)
        df = df.transpose()
        x1 = df['lat'].tolist()
        y1 = df['lng'].tolist()
        text = (df['occupied_ratio']*100).tolist()

    return [
        {'type': 'scattermapbox','name': 'Charging Station Occupied Ratio',
        'lat': x1,
        'lon': y1,
        'text': text,
        'marker': { 'color': "red", 'size': 5 }}
    ]


def test_fct():
    return [{'y': [
    0.05943275750876332473 * 100,
    0.04712317096368065783 * 100,
    0.04244929596970110481 * 100,
    0.04810573870890297678 * 100,
    0.02563388334773649259 * 100,
    0.02294805453940804789 * 100,
    0.06464654698386771179 * 100,
    0.01896241171045365576 * 100, 
    0.05660705272141365258 * 100], 
    'x': [
        'Grosszentren',
        'Nebenzentren der Grosszentren',
        'Gürtel der Grosszentren',
        'Mittelzentren',
        'Gürtel der Mittelzentren',
        'Kleinzentren',
        'Periurbane ländliche Gemeinden',
        'Agrargemeinden',
        'Touristische Gemeinden'
    ], 'type': 'bar'}]

@app.route('/hourBarPlot', methods=['GET'])
def hourBarPlot():
    return json.dumps(hour_profile())

@app.route('/hourBarPlotWE', methods=['GET'])
def hourBarPlotWE():
    return json.dumps(hour_profile_WE())

@app.route('/latLong', methods=['GET'])
def latLong():
    return json.dumps(lat_lon())

@app.route('/plot1', methods=['GET'])
def plot1():
    return jsonify(plot_distribution_charging_begin_day('15_20', df_clean))

@app.route('/plot2', methods=['GET'])
def plot2():
    return jsonify(plot_distribution_charging_begin_day('12_17', df_clean))

@app.route('/plot3', methods=['GET'])
def plot3():
    return jsonify(plot_distribution_charging_begin_hour('4_9', df_clean))

@app.route('/plot4', methods=['GET'])
def plot4():
    return jsonify(plot_distribution_charging_begin_hour('6_11', df_clean))

@app.route('/plot5', methods=['GET'])
def plot5():
    return jsonify(plot_distribution_programmed_charging('5_10', df_clean))

@app.route('/plot6', methods=['GET'])
def plot6():
    return jsonify(plot_distribution_programmed_charging('18_23', df_clean))

@app.route('/plot7', methods=['GET'])
def plot7():
    return jsonify(plot_percentage_maxcharge('5_10', df_clean))

@app.route('/plot8', methods=['GET'])
def plot8():
    return jsonify(plot_percentage_maxcharge('11_16', df_clean))

@app.route('/plota', methods=['GET'])
def plota():
    return jsonify(total_consumption_plt(df_clean))

@app.route('/plotb', methods=['GET'])
def plotb():
    return jsonify(charging_amount_plt(df_clean))

@app.route('/plotc', methods=['GET'])
def plotc():
    return jsonify(overall_load_curve_plt(load_curve_df))

@app.route('/plotd', methods=['GET'])
def plotd():
    return jsonify(median_load_energy_plt(load_curve_df))

@app.route('/privWE', methods=['GET'])
def privWE():
    return jsonify(plot_hourly_consumption(df_clean))

@app.route('/erica', methods=['GET'])
def erica():
    return jsonify(charge_type_v_cid(df_clean))

@app.route('/', methods=['GET'])
def index():
    return jsonify(test_fct())

@app.route('/private', methods=['POST'])
def getById():
    if request.method == 'POST':
        id = request.get_json().get('id')
        return json.dumps(plot_consumption_history(id, df_clean))


if __name__ == '__main__':
    app.run()