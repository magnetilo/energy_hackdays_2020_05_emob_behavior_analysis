# Energy Hackdays 2020 Group 05 e-mobility behavior analysis
Erica Lastufka, physics @ www.fhnw.ch | Florence Meier, Full Stack Developmant (focus on frontend) | Benedikt Ramsauer, Data Scientist @ www.swiss-sdi.ch | Xavier Bays, Data Scientist @ www.swiss-sdi.ch | Tim Breitenbach, Analytics & Data Architect @ www.axpo.ch | Pradip Ravichandran, Computer Science @ www.fhnw.ch | Thilo Weber, Data Scientist @ www.geoimpact.ch | David Suter, Sustainable Energy Specialist @ www.geoimpact.ch 

## Dashboard Sreenshots

![sreenshot1](imgs/Screenshot from 2020-08-29 15-06-20.png)

![sreenshot2](imgs/Screenshot from 2020-08-29 15-06-47.png)

![sreenshot3](imgs/Screenshot from 2020-08-29 15-07-14.png)

![sreenshot4](imgs/Screenshot from 2020-08-29 15-07-44.png)

![sreenshot5](imgs/Screenshot from 2020-08-29 15-08-04.png)

![sreenshot6](imgs/Screenshot from 2020-08-29 15-08-21.png)


## findings

### public ev charging station

- Typology of municipalities is an important feature for occupied ratio
- highest occupied ratio in big centers and peri-urban rural communes
- no correlation between population density and occupied ratio
- different patterns on weekdays and weekends

### private ev charging station
Different charging patterns of private customers:
- Charging needs
- Hours of charging
- Week days of charging

This provide good hints for a further automated customer segmentation.

### comparison of privat & public charging behavior
- different time-profile on weekdays and weekend in public, but not in private

## possible next steps

### public ev charging station
- occupation forecast for every charging station (hourly based day profile as a new feature for the website www.ich-tanke-strom.ch ) --> for the customers
- clustering with more location-based data (socio-economic, roads, traffic etc.), understanding of different charging patterns --> for the provider
- compare clusters of charging behavior with pv potential and production profiles, possibility of own consumption of charging stations --> for the grid

### private ev charging station
- automated customer segmentation based on linked information (building data, socio-economoic data, location) --> for the provider
- cost estimation tool for customer --> for the customer
- prediction of behavior changes for the load-curve --> for the grid


## faced challenges
- parsing and structuring provided raw data --> long running tasks
- handling data errors and missing data

## things to do
- run everything on database server
- productionalize frontend to shoot queries onto database and parse them to json 

        
## Data Engineering

### Architecture Overview

![Overview](/data_engineering_diemo/data_eng_architecture.png)
data_engineering_diemo/data_eng_architecture.png

### Data Structure of diemo jsons

- EVSEStatuses
    - OperatorID 
    - Operatorname
    - EVSEStatusRecord
        - EVSEID
        - EVSEStatus
        
### Python and SQL part
For parsing the 48'000 json files in 5 minutes resolution for 6 months we used python scripts.
We had to implement various exceptions because of empty jsons.

First we tried looping everything into csv, which did not perform as fast as we would like.
We then tried Apache Feather as a data transfer format but the data storage speed wasn't the problem.
The next try was a sqlite database which works fine and was an okay solution for the hackathon.
If the project would go live, we would recommend a database server preferably in the cloud, to get the inital data loading done quick.
The dataload still takes over 10 hours and is not very efficient.

### SQL Queries
The first query is about getting an overlook over all the EV-Charging points, the different operators.

## Visualisation ideas  

### public ev charging stations
- snapshot for specific time (occupied, available) on a map
- top 3 utilised stations for each canton on a map
- occupation ratio per station on a map
- time-profile clusters --> which stations have the same time-profile
- time-profile in city centers, countryside and touristic regions
- aggregated occupation over time of a day/week for all stations
- occupation over time of a day/week for a selected station
- typically duration of a charging process on a map


## Analyses

### Charging points utilization

Features analysis:

![extraTreesRegressor](/public_metrics_features_analysis/ExtraTreesRegressor.png)


Legend:

1 | Grosszentren

2 | Nebenzentren der Grosszentren

3 | Gürtel der Grosszentren

4 | Mittelzentren

5 | Gürtel der Mittelzentren

6 | Kleinzentren

7 | Periurbane ländliche Gemeinden

8 | Agrargemeinden

9 | Touristische Gemeinden


Occupied ration distribution:

![occupied_ratio_distribution](imgs/occupied_ratio_distribution.png)

Weekend VS weekdays behaviour for private customers: hourly consumption:

![hourly_consumption](imgs/hourly_consumption.png)

Example of behaviour differences between two private customers: Distribution of the percentage of the whole battery that is charged.

![percentage_of_max_charge_1](imgs/percentage_of_max_charge_1.png)

![percentage_of_max_charge_2](imgs/percentage_of_max_charge_2.png)

Load curve for private customers:

![ecars_load_curve](imgs/ecars_load_curve.png)

Overall energy consumption by private e-cars. This also show the adoption curve. The red zone corresponds to COVID time.

![total_consumption](imgs/total_consumption.png)

