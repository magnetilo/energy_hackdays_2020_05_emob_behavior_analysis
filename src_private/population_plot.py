"""Coputation and plots for the whole population analysis"""

from src_private.config import COVID_END, COVID_START

# Total comsumption

def total_consumption(df_clean):
    """Compute the overall consumption by date"""
    
    return df_clean.groupby('timestamp')['increment'].sum()

def total_consumption_plt(df_clean):
    """Scatter plot of the total consumption"""
    total_cons = total_consumption(df_clean)
    
    data = [{
        'x':total_cons.index.values.tolist(),
        'y': (total_cons.cumsum()/1000).tolist(),
        'mode': 'lines',
        'name': 'total_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'Total Consumption',
        'xaxis': {
            'title': 'Time'
        },
        'yaxis': {
            'title': 'kWh'
        },
        'shapes': [
            {
                'type': "rect",
                'yref': "paper",
                'x0': str(COVID_START),
                'x1': str(COVID_END),
                'y0': 0,
                'y1': 1,
                'line': dict(width=0),
                'fillcolor': "lightpink",
                'opacity': 0.5
            }
        ]
    }
    
    return {'data': data, 'layout': layout}


# Charging Amount

def charging_amount(df_clean):
    """Compute the total amount of energy in (kWh)required for a charging period"""
    
    return (df_clean.groupby(['chargepoint_connector_log'])['increment'].sum()/1000).values

def charging_amount_plt(df_clean):
    """Scatter plot of the total consumption"""
    charging_am = charging_amount(df_clean)
    
    data = [{
        'x':charging_am.tolist(),
        'name': 'Charging amount',
        'type': 'histogram'
    }]
    
    layout = {
        'title':'Distribution of the charging amounts',
        'xaxis': {
            'title': 'kWh/charge'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        }
    }
    
    return {'data': data, 'layout': layout}


# Load Curve

def load_curve(df_clean):
    """Compute statistics for the hourly agregation of the increment"""
    
    return df_clean.groupby('hour')['increment'].agg(['sum', 'count', 'median', 'mean'])

def overall_load_curve_plt(load_curve_df):
    """Scatter plot of the cumulative load function
    
    Parameters
    -----------
    load_curve_df: pandas DataFrame
        Output of the load_curve function.
    """
    
    data = [{
        'x':load_curve_df.index.tolist(),
        'y': (load_curve_df['sum']/1000).tolist(),
        'mode': 'lines',
        'name': 'total_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'Load curve - total amount of energy',
        'xaxis': {
            'title': 'Hours'
        },
        'yaxis': {
            'title': 'Overall kWh'
        },
    }
    
    return {'data': data, 'layout': layout}


def median_load_energy_plt(load_curve_df):
    """Scatter plot of the cumulative load function
    
    Parameters
    -----------
    load_curve_df: pandas DataFrame
        Output of the load_curve function.
    """
    
    data = [{
        'x':load_curve_df.index.tolist(),
        'y': (load_curve_df['median']).tolist(),
        'mode': 'lines',
        'name': 'total_consumption',
        'type': 'scatter'
    }]
    
    layout = {
        'title':'Load curve - Median charging energy',
        'xaxis': {
            'title': 'Hours'
        },
        'yaxis': {
            'title': 'Wh'
        },
    }
    
    return {'data': data, 'layout': layout}



def plot_hourly_consumption(df):
    weekend = df[df['is_weekend']]
    week = df[~df['is_weekend']]
    

    x_data_1 = weekend[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.hour)

    x_data_2 = week[['chargepoint_connector_log', 'charge_start']].drop_duplicates(
            keep='first')['charge_start'].apply(lambda x: x.hour)

    data = [
        {
        'x':x_data_1.tolist(),
        'type': 'histogram',
        'xbins': {'size': 1},
        'name':'weekend'
    },
    {
        'x':x_data_2.tolist(),
        'type': 'histogram',
        'xbins': {'size': 1},
        'name':'weekdays'
    }]
    
    layout = {
        'title':'Hour distribution of the of the charging process for the whole private population',
        'xaxis': {
            'title': 'kWh/charge'
        },
        'yaxis': {
            'title': 'Nb of charging processes'
        }
    }
    
    return {'data': data, 'layout': layout}
