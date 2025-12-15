WITH stocks_info AS (
    SELECT
        TICKER as market_ticker,
        TYPE as market_type,
        NAME as company_name,
        URL as scraped_from
    FROM {{ source('src_stocks_info', 'STOCKS_INFO') }}
)

SELECT
    *
FROM stocks_info
