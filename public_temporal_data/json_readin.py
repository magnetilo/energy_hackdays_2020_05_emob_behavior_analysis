import pandas as pd

df_total = pd.DataFrame()
with open('hour_profile_per_region_per_weektime.json') as f:
    df = pd.read_json(f)
    df = df.transpose()
    city_center = df[df['region'] == 'city centers']
    city_center_weekdays = city_center[city_center['weektime'] == 'weekday']
    x1 = city_center_weekdays['hour']
    y1 = city_center_weekdays['occupied_ratio']
    title1 = 'City Center Weekday'