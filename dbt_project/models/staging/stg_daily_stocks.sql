WITH stocks AS (
    SELECT
        *
    FROM {{ source('src_stocks_info', 'STOCKS_INFO') }}
)

SELECT
    *
FROM stocks
