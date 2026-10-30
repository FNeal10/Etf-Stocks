SELECT
    ticker,
    market_type,
    market_name,
    market_url
FROM {{ ref('stg_market_urls') }}