import csv
import json

csvfile = open('hour_profile_per_region_per_weektime.csv', 'r', encoding='utf-8')
jsonfile = open('hour_profile_per_region_per_weektime.json', 'w', encoding='utf-8')

#fieldnames = ("municipal_typologie_id","municipal_typologie","num_occupied","num_tot","occupied_ratio")
reader = csv.DictReader(csvfile)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')