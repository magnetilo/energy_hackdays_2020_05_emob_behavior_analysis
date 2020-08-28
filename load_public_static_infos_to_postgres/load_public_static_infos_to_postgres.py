#%%
import urllib.request
import json
import pandas as pd
#import flat_table
import itertools
import psycopg2


#%%
public_statis_data_url = 'https://data.geo.admin.ch/ch.bfe.ladestellen-elektromobilitaet/data/oicp/ch.bfe.ladestellen-elektromobilitaet.json'

with urllib.request.urlopen(public_statis_data_url) as url:
    # string = url.read().decode()
    # print(string)
    data = json.loads(url.read().decode())


nested_df = pd.json_normalize(data, "EVSEData")

flat_df_OperatorID = pd.DataFrame(list(itertools.chain(*nested_df.apply(lambda row: [row['OperatorID']]*len(row['EVSEDataRecord']), axis=1).to_list())), columns=['OperatorID'])
flat_df_OperatorName = pd.DataFrame(list(itertools.chain(*nested_df.apply(lambda row: [row['OperatorName']]*len(row['EVSEDataRecord']), axis=1).to_list())), columns=['OperatorName'])
flat_df_EVSEDataRecord = pd.DataFrame(pd.concat([pd.json_normalize(x) for x in nested_df["EVSEDataRecord"]]))
flat_df_EVSEDataRecord = pd.DataFrame(flat_df_EVSEDataRecord.values, columns=flat_df_EVSEDataRecord.columns)

flat_df = pd.concat([flat_df_OperatorID, flat_df_OperatorName, flat_df_EVSEDataRecord], axis=1)

#flat_df.to_csv('public_static_infos.csv')

#flat_df = flat_table.normalize(nested_df, expand_lists=True, expand_dicts=True)
#print(flat_df)

#%%
with open('dbaccess.config') as file:
    connection_string = file.read()

conn = psycopg2.connect(connection_string)
with conn.cursor() as cur:
    flat_df2 = flat_df.copy()
    flat_df2["ChargingFacilities"] = flat_df2["ChargingFacilities"].apply(lambda x: json.dumps(x))
    #flat_df2["AdditionalInfo"] = flat_df2["AdditionalInfo"].apply(lambda x: json.dumps(x))
    flat_df2['OperatorName'] = flat_df2['OperatorName'].apply(lambda x: x.replace("'", "''") if x is not None else x)
    flat_df2['Address.City'] = flat_df2['Address.City'].apply(lambda x: x.replace("'", "''") if x is not None else x)
    flat_df2['Address.Street'] = flat_df2['Address.Street'].apply(lambda x: x.replace("'", "''") if x is not None else x)
    flat_df2['ChargingStationName'] = flat_df2['ChargingStationName'].apply(lambda x: x.replace("'", "''") if x is not None else x)

    value_string = ','.join(flat_df2.drop(['AdditionalInfo', 'EnChargingStationName',
                                           'ChargingModes', 'MaxCapacity'], axis=1).apply(lambda x: "(\
'{}', '{}', {}, '{}',\
'{}', '{}', '{}', '{}',\
'{}', '{}', array{},\
'{}', '{}', {}, '{}',\
'{}', array{},\
'{}', '{}', array{},\
array{}, '{}', '{}', '{}',\
'{}', '{}', '{}', '{}',\
'{}', st_pointfromtext('POINT({})', 4326), '{}'\
)".format(*x), axis=1).values.tolist()).replace('arrayNone', 'Null')

    cur.execute(
        """
            insert into ladestationen_elektromobilitaet.static_data
            values {values};
        """.format(
            values=value_string
        )
    )

conn.commit()
conn.close()