import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def get_private_ids(df):
    """Get all the unique connectors"""
    return df['chargepoint_connector'].unique().tolist()

def id_subset(my_customer, df):
    """Filter dataframe on 1 single id"""
    sub_df = df[df['chargepoint_connector'] == my_customer].copy()
    return(sub_df)


def plot_consumption_history(my_customer, df):
    """Plot Consumption history for a single customer"""
    sub_df = id_subset(my_customer, df)

    data = [{
        'x':sub_df['timestamp'].astype(str).tolist(),
        'y': sub_df['metervalue'].tolist(),
        'mode': 'markers',
        'name': 'historical_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'Consumption history (with plugging)',
        'xaxis': {
            'title': 'Time'
        },
        'yaxis': {
            'title': 'Wh'
        },
    }

    return {'data': data, 'layout': layout}


def plot_charging_history(my_customer, df):
    """Plot charging history (without plugging time)"""
    sub_df = id_subset(my_customer, df)
    sub_df_charging = sub_df[sub_df['is_charging'] == 1].copy()

    data = [{
        'x':sub_df_charging['timestamp'].astype(str).tolist(),
        'y': sub_df_charging['metervalue'].tolist(),
        'mode': 'markers',
        'name': 'charging_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'Charging history: {}'.format(my_customer),
        'xaxis': {
            'title': 'Time'
        },
        'yaxis': {
            'title': 'Wh'
        },
    }

    return {'data': data, 'layout': layout}


def plot_distribution_charging_begin_day(my_customer, df):
    sub_df = id_subset(my_customer, df)

    x_data = sub_df[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.weekday())


    data = [{
        'x':x_data.tolist(),
        'name': 'Weekly charging amount',
        'type': 'histogram',
        'xbins': {'size': 1}
    }]
    
    layout = {
        'title':'Day distribution of the of the charging process [monday = 0, ...]',
        'xaxis': {
            'title': 'Weekday'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}




def plot_distribution_charging_begin_hour(my_customer, df):
    sub_df = id_subset(my_customer, df)

    x_data = sub_df[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.hour)

    data = [{
        'x':x_data.tolist(),
        'name': 'Hourly charging count',
        'type': 'histogram',
        'xbins': {'size': 1}
    }]
    
    layout = {
        'title':'Hour distribution of the of the charging process',
        'xaxis': {
            'title': 'Hour'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}


def plot_charging_time_distribution(my_customer, df):
    sub_df = id_subset(my_customer, df)
    x_data = sub_df[['chargepoint_connector_log', 'charging_time']].drop_duplicates(
            keep='first')['charging_time'].apply(lambda x: x.days * 24 + x.seconds / 3600)

    data = [{
        'x':x_data.tolist(),
        'name': 'Hourly charging count',
        'type': 'histogram',
        'xbins': {'size': 1}
    }]
    
    layout = {
        'title':'Time distribution of the of the charging time [hours]',
        'xaxis': {
            'title': 'Charging time [hour]'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}


def plot_distribution_programmed_charging(my_customer, df):
    sub_df = id_subset(my_customer, df)

    x_data = sub_df[['chargepoint_connector_log', 'use_programmed_start']
                 ].drop_duplicates(keep='first')['use_programmed_start']

    data = [{
        'x':x_data.tolist(),
        'name': 'Hourly charging count',
        'type': 'histogram',
        'histnorm': 'probability density'
    }]
    
    layout = {
        'title':'Distribution of use of programmed charging',
        'xaxis': {
            'title': 'Charging time [hour]'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}


def plot_energy_by_charge_distribution(my_customer, df):
    sub_df = id_subset(my_customer, df)
    x_data = sub_df.groupby('chargepoint_connector_log')['increment'].sum()


    data = [{
        'x':x_data.tolist(),
        'name': 'Hourly charging count',
        'type': 'histogram',
        'xbins': {'size': 1000}
    }]
    
    layout = {
        'title':'Distribution of energy consummed by charge [Wh]',
        'xaxis': {
            'title': 'Wh'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}


def plot_percentage_maxcharge(my_customer, df):

    sub_df = id_subset(my_customer, df)
    x_data = sub_df.groupby('chargepoint_connector_log')['increment'].sum() / sub_df.groupby('chargepoint_connector_log')['increment'].sum().max()

    data = [{
        'x':x_data.tolist(),
        'name': 'Hourly charging count',
        'type': 'histogram',
        'xbins': {'size': 0.1}
    }]
    
    layout = {
        'title':'Percentage of max charge [% of Wh]',
        'xaxis': {
            'title': 'Wh'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        },
    }

    return {'data': data, 'layout': layout}


def plot_monthly_cost(my_customer, df):

    sub_df = id_subset(my_customer, df)

    sub_df = sub_df[sub_df['year'] == 2020].copy()
    total_costs = sub_df.groupby('month')['cost'].sum().sum()

    data = [{
        'x':sub_df.groupby('month')['cost'].sum().index.values.tolist(),
        'y': sub_df.groupby('month')['cost'].sum().tolist(),
        'mode': 'markers',
        'name': 'charging_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'2020 monthly costs [CHF] (Total costs = {} CHF)'.format(
        round(total_costs, 2)),
        'xaxis': {
            'title': 'Month'
        },
        'yaxis': {
            'title': 'CHF'
        },
    }

    return {'data': data, 'layout': layout}
