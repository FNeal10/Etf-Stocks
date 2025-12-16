{{
    config(
        materialized='incremental',
        unique_key = ['Ticker','Trade_Date']
    )
}}

with 

ohclv_data as (
    select
    Ticker,
    Trade_Date,
    Open_Price,
    High_Price,
    Low_Price,
    Close_Price,
    Trade_Volume,
    Price_Change_Pct,
    High_Low_Range_Pct,
    Close_Open_Range_Pct,
    Percent_Change_Pct
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > ( select coalesce(max(Trade_Date), '1900-01-01') from {{ this }})
    {% endif %}
)

select
*
from ohclv_data
