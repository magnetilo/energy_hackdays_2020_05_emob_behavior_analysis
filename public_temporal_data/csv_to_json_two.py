import json
import pandas as pd


df = pd.read_csv('hour_profile_for_3cities_per_weektime.csv', encoding='utf-8')
result = df.to_json(orient="index")
parsed = json.loads(result)


with open('hour_profile_for_3cities_per_weektime.json', 'w', encoding='utf-8') as json_file:
  json.dump(parsed, json_file, indent=4)