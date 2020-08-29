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

    trace = go.Scatter(
        x=sub_df['timestamp'],
        y=sub_df['metervalue'],
        mode='markers')

    data = [trace]

    layout = go.Layout(title='Consumption history (with plugging)')

    fig = go.Figure(data=data, layout=layout)

    fig.show()


def plot_charging_history(my_customer, df):
    """Plot charging history (without plugging time)"""
    sub_df = id_subset(my_customer, df)
    sub_df_charging = sub_df[sub_df['is_charging'] == 1].copy()
    trace = go.Scatter(
        x=sub_df_charging['timestamp'],
        y=sub_df_charging['metervalue'],
        mode='markers')

    data = [trace]

    layout = go.Layout(title='Charging history: {}'.format(my_customer))

    fig = go.Figure(data=data, layout=layout)

    fig.show()


def plot_distribution_charging_begin_day(my_customer, df):
    sub_df = id_subset(my_customer, df)

    data = go.Histogram(
        x=sub_df[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.weekday()),
        xbins={'size': 1}
    )

    layout = go.Layout(
        title='Day distribution of the of the charging process [monday = 0, ...]')

    fig = go.Figure(data=data, layout=layout)

    fig.show()


def plot_distribution_charging_begin_hour(my_customer, df):
    sub_df = id_subset(my_customer, df)

    data = go.Histogram(
        x=sub_df[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.hour),
        xbins={'size': 1}
    )

    layout = go.Layout(
        title='Hour distribution of the of the charging process')

    fig = go.Figure(data=data, layout=layout)

    fig.show()


def plot_charging_time_distribution(my_customer, df):
    sub_df = id_subset(my_customer, df)
    data = go.Histogram(
        x=sub_df[['chargepoint_connector_log', 'charging_time']].drop_duplicates(
            keep='first')['charging_time'].apply(lambda x: x.days * 24 + x.seconds / 3600),
        xbins={'size': 1}
    )

    layout = go.Layout(
        title='Time distribution of the of the charging time [hours]')

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_distribution_programmed_charging(my_customer, df):
    sub_df = id_subset(my_customer, df)

    data = go.Histogram(
        x=sub_df[['chargepoint_connector_log', 'use_programmed_start']
                 ].drop_duplicates(keep='first')['use_programmed_start'],
        histnorm='probability density')

    layout = go.Layout(title='Distribution of use of programmed charging')

    fig = go.Figure(data=data, layout=layout)

    fig.show()


def plot_energy_by_charge_distribution(my_customer, df):
    sub_df = id_subset(my_customer, df)
    data = go.Histogram(
        x=sub_df.groupby('chargepoint_connector_log')['increment'].sum(),
        xbins={'size': 1000}
    )

    layout = go.Layout(title='Distribution of energy consummed by charge [Wh]')

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_percentage_maxcharge(my_customer, df):

    sub_df = id_subset(my_customer, df)
    data = go.Histogram(
        x=sub_df.groupby('chargepoint_connector_log')['increment'].sum(
        ) / sub_df.groupby('chargepoint_connector_log')['increment'].sum().max(),
        xbins={'size': 0.1}
    )

    layout = go.Layout(title='Percentage of max charge [% of Wh]')

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_monthly_cost(my_customer, df):

    sub_df = id_subset(my_customer, df)

    sub_df = sub_df[sub_df['year'] == 2020].copy()

    data = [go.Scatter(
        x=sub_df.groupby('month')['cost'].sum().index.tolist(),
        y=sub_df.groupby('month')['cost'].sum().values)]

    total_costs = sub_df.groupby('month')['cost'].sum().values.sum()
    layout = go.Layout(title='2020 monthly costs [CHF] (Total costs = {} CHF)'.format(
        round(total_costs, 2)))

    fig = go.Figure(data=data, layout=layout)
    fig.show()
