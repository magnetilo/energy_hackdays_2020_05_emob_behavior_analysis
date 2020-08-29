"""Contains loading and data processing functions for private data"""

import datetime

import numpy as np
import pandas as pd

COVID_START = datetime.datetime(2020, 3, 15, 0, 0, 0)
COVID_END = datetime.datetime(2020, 4, 30, 23, 59, 59)


def load_private(data_path):
    """Load private data set from csv file semicolon separated"""
    return pd.read_csv(data_path, sep=";")


def data_preprocess(df):
    """Contains all the pre process for the dataframe."""

    # Convert string timestamp  to datetime type
    df['timestamp'] = df['timestamp'].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M"))

    # Create a unique id for a chargepoint
    df['chargepoint_connector'] = df['chargepoint'].apply(
        lambda x: str(x)) + '_' + df['connector'].apply(lambda x: str(x))

    # Create a unique id for chargepoint, connector and log
    df['chargepoint_connector_log'] = 'customer_' + df['chargepoint_connector'].apply(
        lambda x: str(x)) + '_' + df['charge_log_id'].apply(lambda x: str(x))

    # Add some time related informaiton
    df['weekday'] = df['timestamp'].dt.weekday
    df['hour'] = df['timestamp'].dt.hour
    df['month'] = df['timestamp'].dt.month
    df['during_corona'] = (COVID_START <= df['timestamp']
                           ) & (df['timestamp'] <= COVID_END)

    # Create a variable telling if the car is charging
    df['is_charging'] = df['increment'] > 500

    # Remove extrem values
    df['is_extrem_value'] = df['increment'] > 5000

    # Keep only data from 2019 (we have one outlier in 2014)
    df = df[df['timestamp'] >= pd.Timestamp('2019-01-01 00:00:00')].copy()

    # When increment is under 0 correct it by giving value of 0
    df.loc[df['increment'] < 0, 'increment'] = 0

    # Hochtarif vs Niedertarif
    # Following values are not correct
    # Also 7h-20h  is not true for saturday
    hochtarif = 0.2  # CHF by kwh
    niedertarif = 0.1  # CHF by kwh
    df['is_hochtarif'] = df['timestamp'].apply(
        lambda x: (x.hour >= 7) & (x.hour <= 20))
    df['tarif'] = niedertarif
    df.loc[df['is_hochtarif'] == True, 'tarif'] = hochtarif
    df['cost'] = df['increment'] * df['tarif'] / 1000

    df.sort_values(by=['timestamp', 'connector', 'chargepoint',
                       'charge_log_id'], ascending=True, inplace=True)

    # Charging start, end time and duration
    # We also remove charging time that last more than 12 hours
    charging_length = df[df['is_charging']].groupby('chargepoint_connector_log')[
        'timestamp'].agg([min, max])
    charging_length.rename(
        columns={'min': 'charge_start', 'max': 'charge_end'}, inplace=True)
    charging_length['charging_time'] = charging_length['charge_end'] - \
        charging_length['charge_start']
    charging_length['is_too_long_charging'] = charging_length['charging_time'] > datetime.timedelta(
        hours=12)

    df = pd.merge(df, charging_length, on='chargepoint_connector_log')

    # Use of programmed charging
    comparing_time = df.loc[df['chargepoint_connector_log'].drop_duplicates(
        keep='first').index, ['chargepoint_connector_log', 'charge_start', 'timestamp']].copy()
    comparing_time['use_programmed_start'] = (
        comparing_time['charge_start'] - comparing_time['timestamp']).apply(lambda x: x.seconds / 3600) > 0.25
    df = df.merge(on='chargepoint_connector_log', right=comparing_time[[
                  'chargepoint_connector_log', 'use_programmed_start']], how='left')

    return df
