
create schema ladestationen_elektromobilitaet;

create table ladestationen_elektromobilitaet.static_data (
    OperatorID text,
    OperatorName text,
    IsOpen24Hours boolean,
    ChargingStationId text,
    lastUpdate text,
    HotlinePhoneNum text,
    ClearinghouseID text,
    OpeningTimes text,
    ChargingStationName text,
    --EnChargingStationName text,
    HubOperatorID text,
    Plugs text[],
    Accessibility text,
    EvseID text,
    DynamicInfoAvailable boolean,
    ChargingFacilities json,
    IsHubjectCompatible boolean,
    --ChargingModes text[],
    --MaxCapacity text,
    PaymentOptions text[],
    --AdditionalInfo json,
    ChargingPoolID text,
    deltaType text,
    ValueAddedServices text[],
    AuthenticationModes text[],
    Address_City text,
    Address_Country text,
    Address_HouseNum text,
    Address_PostalCode text,
    Address_Street text,
    Address_Floor text,
    Address_Region text,
    Address_Timezone text,
    geom geometry(POINT, 2056),
    geom_point_entrance text
);

alter table ladestationen_elektromobilitaet.static_data add primary key (EvseID);
--create index idx_static_data_evseid on ladestationen_elektromobilitaet.static_data using btree (EvseID);
create index indexg_static_data_geom on ladestationen_elektromobilitaet.static_data using gist (geom);

create table ladestationen_elektromobilitaet.temporal_data (
    index int,
    EVSEStatus text,
    EvseID text,
    OperatorID text,
    OperatorName text,
    timestamp timestamp
);

create index idx_temporal_data_evseid on ladestationen_elektromobilitaet.temporal_data using btree (EvseID);
create index idx_temporal_data_timestamp on ladestationen_elektromobilitaet.temporal_data using gist (timestamp);


-- public stations time aggregations:
create table ladestationen_elektromobilitaet.temporal_data_count_evseid as 
select evseid, evsestatus, count(*) as num_timestamps   
from ladestationen_elektromobilitaet.temporal_data 
group by evseid, evsestatus 
order by evseid;

create table ladestationen_elektromobilitaet.count_status_per_operator as
select OperatorID, OperatorName, evsestatus,
       count(*) as num_timestamps
from ladestationen_elektromobilitaet.temporal_data
group by OperatorID, OperatorName, evsestatus 
order by OperatorID, evsestatus;



create table ladestationen_elektromobilitaet.count_status_per_hour_of_day as
select evseid, evsestatus, 
       date_part('hour', timestamp) as hour,
       count(*) as num_timestamps
from ladestationen_elektromobilitaet.temporal_data
group by evseid, evsestatus, date_part('hour', timestamp);



create table ladestationen_elektromobilitaet.count_status_per_hour_of_weekday as
select evseid, evsestatus, 
       date_part('hour', timestamp) as hour,
       to_char(timestamp::date + 1541990258312/1000 * interval '1 second', 'day') as weekday,
       count(*) as num_timestamps
from ladestationen_elektromobilitaet.temporal_data
group by evseid, evsestatus, 
         date_part('hour', timestamp), 
         to_char(timestamp::date + 1541990258312/1000 * interval '1 second', 'day');








create table ladestationen_elektromobilitaet.temporal_data_count_evseid as 
select evseid, evsestatus, count(*) as num_timestamps
from ladestationen_elektromobilitaet.temporal_data 
group by evseid, evsestatus order by evseid;




-- public stations metric and features table:
create table ladestationen_elektromobilitaet.metrics_and_features as
select evseid, operatorname, a.geom, st_y(a.geom) as lat, st_x(a.geom) as lng, 
       num_occupied, num_tot,
       chargingfacilities->0->>'power' as power, 
       typ as municipal_typologie, 
       bbtot as population_hect,
       occupied_ratio
from ladestationen_elektromobilitaet.static_data a 
join geostat.gde_typologien b on st_contains(b.geom, a.geom) 
join geostat.statpop_hect c on st_contains(c.geom, a.geom)
join (
    select evseid, 
           --1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(num_timestamps) as occupied_ratio
           sum(case when evsestatus='Occupied' then num_timestamps else 0 end) as num_occupied,
           sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as num_tot,
           1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as occupied_ratio
    from ladestationen_elektromobilitaet.temporal_data_count_evseid 
    group by evseid
    having sum(case when evsestatus in ('Occupied', 'Available') then 1 else 0 end)>0
) z using(evseid)
where cardinality(plugs) = 1;




create table ladestationen_elektromobilitaet.public_day_profile_per_gdetyp as
select typ as municipal_typologie,
       sum(case when evsestatus='Occupied' then num_timestamps else 0 end) as num_occupied,
       sum(case when evsestatus in ['Occupied', 'Available'] then num_timestamps else 0 end) as num_tot,
       1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(case when evsestatus in ['Occupied', 'Available'] then num_timestamps else 0 end)
from ladestationen_elektromobilitaet.count_status_per_hour_of_day a
join ladestationen_elektromobilitaet.metrics_and_features b using (evseid)
group by typ
order by typ;




-- Output: --------------------------------------------
-- occupied_ratio per municipal_typologie
select municipal_typologie as municipal_typologie_id,
	   case when municipal_typologie = 1 then 'Grosszentren'
       	    when municipal_typologie = 2 then 'Nebenzentren der Grosszentren'
       	    when municipal_typologie = 3 then 'Gürtel der Grosszentren'
       	    when municipal_typologie = 4 then 'Mittelzentren'
       	    when municipal_typologie = 5 then 'Gürtel der Mittelzentren'
       	    when municipal_typologie = 6 then 'Kleinzentren'
       	    when municipal_typologie = 7 then 'Periurbane ländliche Gemeinden'
       	    when municipal_typologie = 8 then 'Agrargemeinden'
       	    when municipal_typologie = 9 then 'Touristische Gemeinden'
       else 'None' end as municipal_typologie,
       sum(case when evsestatus='Occupied' then num_timestamps else 0 end) as num_occupied,
       sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as num_tot,
       1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as occupied_ratio
from ladestationen_elektromobilitaet.count_status_per_hour_of_day a
join ladestationen_elektromobilitaet.metrics_and_features b using (evseid)
group by municipal_typologie
order by municipal_typologie;


-- weekday_profile per municipal_typologie
select municipal_typologie as municipal_typologie_id,
	   case when municipal_typologie = 1 then 'Grosszentren'
       	    when municipal_typologie = 2 then 'Nebenzentren der Grosszentren'
       	    when municipal_typologie = 3 then 'Gürtel der Grosszentren'
       	    when municipal_typologie = 4 then 'Mittelzentren'
       	    when municipal_typologie = 5 then 'Gürtel der Mittelzentren'
       	    when municipal_typologie = 6 then 'Kleinzentren'
       	    when municipal_typologie = 7 then 'Periurbane ländliche Gemeinden'
       	    when municipal_typologie = 8 then 'Agrargemeinden'
       	    when municipal_typologie = 9 then 'Touristische Gemeinden'
       else 'None' end as municipal_typologie,
       weekday, hour,
       sum(case when evsestatus='Occupied' then num_timestamps else 0 end) as num_occupied,
       sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as num_tot,
       1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as occupied_ratio
from ladestationen_elektromobilitaet.count_status_per_hour_of_weekday a
join ladestationen_elektromobilitaet.metrics_and_features b using (evseid)
where evsestatus in ('Occupied', 'Available')
group by municipal_typologie, weekday, hour
order by municipal_typologie, weekday, hour;


-- hour profile per weektime per region:
select region, weektime, hour,
       sum(case when evsestatus='Occupied' then num_timestamps else 0 end) as num_occupied,
       sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as num_tot,
       1.0*sum(case when evsestatus='Occupied' then num_timestamps else 0 end) / sum(case when evsestatus in ('Occupied', 'Available') then num_timestamps else 0 end) as occupied_ratio
from (
    select evseid,
            evsestatus
           case when municipal_typologie in (1,2) then 'city centers'
                when municipal_typologie in (7,8) then 'country side'
                when municipal_typologie in (9) then 'touristic'
           else 'rest' end as region,
           case when weekday in ('monday','tuesday','wednesday','thursday','friday') then 'weekday'
           else 'weekend' end as weektime,
           hour,
           num_timestamps
    from ladestationen_elektromobilitaet.count_status_per_hour_of_weekday a
    join ladestationen_elektromobilitaet.metrics_and_features b using (evseid)
) c
group by region, weektime, hour
order by region, weektime, hour;



-- hour profile for



-- occupied_ratio per lat lng:
select evseid, operatorname, st_y(st_transform(a.geom, 4326)) as lat, st_x(st_transform(a.geom, 4326)) as lng, occupied_ratio
from ladestationen_elektromobilitaet.metrics_and_features
order by occupied_ratio desc;



-- top ten switzerland:
select 








-- top three canton:
select * 
from (
    select evseid, operatorname, canton, a.geom, st_y(a.geom) as lat, st_x(a.geom) as lng, power, municipal_typologie, population_hect, occupied_ratio,
           ROW_NUMBER() OVER (PARTITION BY section_id ORDER BY canton, occupied_ratio is not null, occupied_ratio desc) AS rank
    from ladestationen_elektromobilitaet.metrics_and_features a 
    join boundaries.kantone b on st_contains(a.geom, b.geom)
) c 
where rank < 4;












