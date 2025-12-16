{{
    config(
        materialized='incremental',
        unique_key=['Ticker','Trade_Date']
    )
}}

with

ema_data as(
    select
    Ticker,
    Trade_Date,
    EMA_5_Day,
    EMA_10_Day,
    EMA_20_Day,
    EMA_50_Day,
    EMA_100_Day,
    EMA_200_Day
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > (
                select coalesce(max(Trade_Date), '1900-01-01') from {{ this }}
        )
    {% endif %}
)

select
*
from ema_data