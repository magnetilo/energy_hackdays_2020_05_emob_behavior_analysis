#%%
import pandas as pd
import json
import flat_table
import os
from pathlib import Path
import psycopg2

#Folder = 'DIEMO'
#directory = os.listdir(Folder)
directory = '../data/DIEMO/DIEMO'
#df_total = pd.DataFrame(columns=['index', 'EVSEStatusRecord.EVSEStatus', 'EVSEStatusRecord.EvseID', 'OperatorID',
#'timestamp'])

#%%
count = 0
num_files = len(os.listdir(directory))
for file in os.listdir(directory):
    #print(file)
    if file in ['.','/','d'] or Path(directory +"\\" + file).stat().st_size == 0:
        print(file + " is damaged")
    else:
        print('count: {} / {}'.format(count, num_files))
        #if count > 0:
        #    break
        count += 1
        #print(Path(Folder +"\\" + file).stat().st_size)
        with open(directory +"\\" + file, "r") as f:
            data = json.load(f)
        df = pd.json_normalize(data, 'EVSEStatuses')
        df_2 = flat_table.normalize(df)
        del df
        df_2['timestamp'] = file[14:33]
        #df_total = df_total.append(df_2,ignore_index=True)

        df_2['OperatorName'] = df_2['OperatorName'].apply(lambda x: x.replace("'", "''") if x is not None else x)
        df_2 = df_2.rename(columns={"EVSEStatusRecord.EVSEStatus": "EVSEStatus", "EVSEStatusRecord.EvseID": "EvseID"})
        #print(df_2.iloc[0,:])
        #print(','.join(df_2.apply(lambda x: "({},'{}','{}','{}','{}','{}')".format(*x), axis=1).values.tolist()))
        value_string = ','.join(df_2.apply(lambda x: "({},'{}','{}','{}','{}',to_timestamp('{}', 'YYYY-MM-DD_HH24_MI_SS'))".format(*x), axis=1).values.tolist())

        with open('dbaccess.config') as file:
            connection_string = file.read()

            conn = psycopg2.connect(connection_string)
            with conn.cursor() as cur:
                cur.execute(
                    """
                        insert into ladestationen_elektromobilitaet.temporal_data
                        values {values};
                    """.format(
                        values=value_string
                    )
                )

            conn.commit()
            conn.close()

        #del df_2
        #print(file + " is done")
#df_total.to_feather('df_total.feather')