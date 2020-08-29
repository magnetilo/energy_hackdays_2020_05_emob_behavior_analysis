SELECT DISTINCT COUNT("EVSEStatusRecord.EvseID") as sum,
       OperatorID,
       OperatorName
FROM main.test
GROUP BY OperatorID, OperatorName