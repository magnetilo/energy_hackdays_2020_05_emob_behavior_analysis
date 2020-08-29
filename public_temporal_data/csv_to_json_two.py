import json
import pandas as pd


df = pd.read_csv('occupied_ratio_per_lat_lng.csv', encoding='utf-8')
result = df.to_json(orient="index")
parsed = json.loads(result)


with open('occupied_ratio_per_lat_lng.json', 'w', encoding='utf-8') as json_file:
  json.dump(parsed, json_file, indent=4)

