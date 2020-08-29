import csv
import json

csvfile = open('occupied_ratio_per_municipality_typology.csv', 'r', encoding='utf-8')
jsonfile = open('occupied_ratio_per_municipality_typology.json', 'w', encoding='utf-8')

fieldnames = ("municipal_typologie_id","municipal_typologie","num_occupied","num_tot","occupied_ratio")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')