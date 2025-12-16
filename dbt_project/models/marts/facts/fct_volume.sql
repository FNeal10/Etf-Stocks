{{
    config(
        matierialized='incremental',
        unique_key=['Ticker','Trade_Date']
    )
}}

with

volume_data as (
    select
    Ticker,
    Trade_Date,
    Trade_Volume,
    Volume_20_Day,
    Volume_50_Day
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > ( 
                select coalesce(max(Trade_Date), '1900-01-01') from {{ this }}
            )
    {% endif %}
)

select 
* 
from volume_data