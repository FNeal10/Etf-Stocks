{{
    config(
        materialized='incremental'
        unique_key=['Ticker','Trade_Date']
    )
}}

with

sma_data as (
    select
    Ticker,
    Trade_Date,
    SMA_5 as SMA_5_Day,
    SMA_10 as SMA_10_Day,
    SMA_20 as SMA_20_Day,
    SMA_50 as SMA_50_Day,
    SMA_100 as SMA_100_Day,
    SMA_200 as SMA_200_Day
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date >
    {% endif %}
)

select 
*
from sma_data