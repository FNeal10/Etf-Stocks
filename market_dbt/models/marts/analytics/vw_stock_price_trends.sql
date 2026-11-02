
SELECT
    ticker,
    date_key,
    price_close,
    sma_7,
    sma_30,
    sma_50

FROM {{ ref('int_stock_moving_averages') }}