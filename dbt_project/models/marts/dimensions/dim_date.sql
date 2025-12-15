{{
    config(
        materialized='incremental',
        unique_key=['Ticker', 'Trade_Date']
    )
}}

with

{% if is_incremental() %}
max_dates as (
    select
        Ticker,
        max(Trade_Date) as last_trade_date
    from {{ this }}
    group by Ticker
),
{% endif %}

trading_dates as (
    select distinct
        s.Ticker,
        s.Trade_Date,
        s.Trade_Year,
        s.Trade_Month,
        s.Trade_Day,
        s.Trade_Day_of_Week,
        s.Trade_Day_of_Year,
        s.Trade_Week_of_Year,
        s.Trade_Quarter,
        s.Is_Start_of_Month,
        s.Is_End_of_Month,
        s.Is_Start_of_Quarter,
        s.Is_End_of_Quarter
    from {{ ref('stg_daily_stock_prices') }} s

    {% if is_incremental() %}
    left join max_dates m
        on s.Ticker = m.Ticker
    where s.Trade_Date > coalesce(m.last_trade_date, '1900-01-01')
    {% endif %}
)

select *
from trading_dates
