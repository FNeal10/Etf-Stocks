SELECT DISTINCT
    date_key,
    transaction_date,
    [year],
    [month],
    [day],
    day_of_week,
    day_of_year,
    week_of_year,
    [quarter],
    is_month_start,
    is_month_end,
    is_quarter_start,
    is_quarter_end
FROM {{ ref('stg_stocks_market_prices') }}