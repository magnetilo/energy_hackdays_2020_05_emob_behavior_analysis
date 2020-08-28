import pandas as pd
import json
import flat_table
import os
from pathlib import Path



def combine(Folder='DIEMO_split'):
    directory = os.listdir(Folder)
    df_total = pd.DataFrame(columns=['index', 'EVSEStatusRecord.EVSEStatus', 'EVSEStatusRecord.EvseID', 'OperatorID',
    'timestamp'])
    for file in directory:
        if Path(Folder +"\\" + file).stat().st_size == 0:
            print(file + " is damaged")
        else:
            #print(Path(Folder +"\\" + file).stat().st_size)
            f = open(Folder +"\\" + file)
            data = json.load(f)
            f.close()
            df = pd.json_normalize(data, 'EVSEStatuses')
            df_2 = flat_table.normalize(df)
            del df
            df_2['timestamp'] = file[14:33]
            df_total = df_total.append(df_2,ignore_index=True)
            del df_2
            print(file + " is done")
    df_total.to_feather('df_total.feather')

combine()