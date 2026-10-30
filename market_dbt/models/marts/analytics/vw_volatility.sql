SELECT
    ticker,
    date_key,
    close_price,
    volatility_20,
    high_price,
    low_price,
    high_price - low_price AS daily_high_low_range,
    CAST(
        (high_price - low_price) * 100.0
        / NULLIF(close_price, 0)
        AS DECIMAL(18, 4)
    ) AS daily_range_pct_of_close
FROM {{ ref('stg_stocks_market_prices') }}