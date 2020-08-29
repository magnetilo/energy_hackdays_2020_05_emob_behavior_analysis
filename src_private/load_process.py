"""Contains loading and data processing functions for private data"""

import datetime

import numpy as np
import pandas as pd


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

    # Create a variable telling if the car is charging
    df['is_charging'] = df['increment'] > 500

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

    return df
