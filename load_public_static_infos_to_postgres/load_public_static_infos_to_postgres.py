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

flat_df.to_csv('public_static_infos.csv')

#flat_df = flat_table.normalize(nested_df, expand_lists=True, expand_dicts=True)
#print(flat_df)


with open('dbaccess.config') as file:
    connection_string = file.read()

conn = psycopg2.connect(connection_string)
with conn.cursor() as cur:
    # Write underground_area_parcel to DB
    if parcels_df.shape[0] > 0:
        value_string = ','.join(
            ["({},{})".format(
                parcelid_sep,
                underground_area_parcel)
                for (parcelid_sep, underground_area_parcel)
                in zip(parcels_df['parcelid_sep'],
                       parcels_df['underground_area'])
            ])
        # print(value_string)

        cur.execute("""
                            update sep_features.parcel_features pf
                            set underground_area_parcel = pu.underground_area_parcel,
                                lastupdated_underground_area = now()
                            from (values {values}) as pu (
                                parcelid_sep, underground_area_parcel)
                            where pf.parcelid_sep = pu.parcelid_sep
                        """.format(values=value_string)
                    )

    # Write underground_geoms_per_parcel to DB
    if underground_geoms_per_parcel_df.shape[0] > 0:
        value_string = ','.join(
            [
                "(default, {}, st_transform(st_simplify(ST_SetSRID(ST_GeomFromGeoJSON('{}'), 21781), 0.5), 2056), now())".format(
                    parcelid_sep,
                    json.dumps(underground_geom))
                for (parcelid_sep, underground_geom)
                in zip(underground_geoms_per_parcel_df['parcelid_sep'],
                       underground_geoms_per_parcel_df['underground_geom'])
            ])
        # print(value_string)

        cur.execute(
            """
                -- Delete already existing entries for analysed parcels
                delete from cadastre_detection.underground_constructions_per_parcel 
                where parcelid_sep in ({parcelids});

                -- Insert underground geometries
                insert into cadastre_detection.underground_constructions_per_parcel (
                    id, parcelid_sep, geom_simple_2056, lastupdated
                )
                values {values};
            """.format(
                parcelids=','.join(underground_geoms_per_parcel_df['parcelid_sep'].astype('str')),
                values=value_string
            )
        )

conn.commit()
conn.close()