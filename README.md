# Energy Hackdays 2020 Group 05 e-mobility behavior analysis

## things to do
- run everything on database server
- productionalize frontend to shoot queries onto database and parse them to json 

## Data Structure of diemo jsons

- EVSEStatuses
    - OperatorID 
    - Operatorname
    - EVSEStatusRecord
        - EVSEID
        - EVSEStatus
        
## Data Engineering

### Architecture Overview

![Overview](https://github.com/magnetilo/energy_hackdays_2020_05_emob_behavior_analysis/tree/master/data_engineering_diemo/data_eng_architecture.png)

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

   
