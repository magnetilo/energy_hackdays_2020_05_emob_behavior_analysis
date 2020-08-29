SELECT "EVSEStatusRecord.EvseID",
       substr(timestamp,0,11) as date,
       substr(timestamp,12,5) as time,
       "EVSEStatusRecord.EVSEStatus",
       OperatorID,
       OperatorName
from main.test
WHERE "EVSEStatusRecord.EvseID" = 'CH*BVS*E001*0001'