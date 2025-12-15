WITH stocks_info AS (
    SELECT
        TICKER,
        TYPE,
        NAME,
        URL
    FROM {{ source('src_stocks_info', 'STOCKS_INFO') }}
)

SELECT
    *
FROM stocks_info
