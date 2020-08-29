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

def classify_charge(df):
    '''classify charge is high, medium, low'''
    df=df[df.is_charging==True]
    median_increment_per_log = pd.DataFrame(df.groupby(['chargepoint_connector_log'])['increment'].agg('median'))
    median_increment_per_log.name = 'median_increment_per_log'
    df = pd.merge(df, median_increment_per_log, on='chargepoint_connector_log', how='left')

    #from this, logical divisions are: low = [0-1e2], mid=[1e2-5e3],high=[>5e3]

    def classify_car_energy(x):
        if x < 1000:
            return 'low'
        elif x < 2000:
            return 'mid'
        elif x < 3000:
            return 'high'
        else:
            return 'extrem'

    df['kWh_type'] = df.increment_y.apply(lambda x: classify_car_energy(x))
    return df


def charge_type_v_cid(df,scale=True):
    '''plot charge type vs chargepoint_connector id in stacked bar plot'''
    df = classify_charge(df)
    xax=df.chargepoint_connector.dropna().unique()
    nlo=np.array([len(df.query("kWh_type == 'low' and chargepoint_connector == @h")) for h in xax])
    nmid=np.array([len(df.query("kWh_type == 'mid' and chargepoint_connector == @h")) for h in xax])
    nhi=np.array([len(df.query("kWh_type == 'high' and chargepoint_connector == @h")) for h in xax])
    nex=np.array([len(df.query("kWh_type == 'extrem' and chargepoint_connector == @h")) for h in xax])

    if scale:
        fac=nlo+nmid+nhi+nex
    else:
        fac=1.
