{{ config(materialized='table') }}

SELECT *
FROM tblStocks
WHERE upper(source) = 'BDO'