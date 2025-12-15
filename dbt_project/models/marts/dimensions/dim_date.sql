{{
    config(
        materialized='incremental',
        unique_key='calendar_date'
    )
}}

with raw_dates as (
    select distinct
    Date as calendar_date,
    Year as calendar_year,
    Month as calendar_month,
    Day as calendar_day,
    DayOfWeek as day_of_week,
    DayOfYear as day_of_year,
    WeekOfYear as week_of_year,
    Quarter as year_quarter,
    IsMonthStart as is_start_of_the_month,
    IsMonthEnd as is_end_of_the_month,
    IsQuarterStart as is_start_of_the_quarter,
    IsQuarterEnd as is_end_of_the_quarter
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Date > (select max(calendar_date) from {{ this }})
    {% endif %}
)
select
    calendar_date,
    calendar_year,
    calendar_month,
    calendar_day,
    day_of_week,
    day_of_year,
    week_of_year,
    year_quarter,
    is_start_of_the_month,
    is_end_of_the_month,
    is_start_of_the_quarter,
    is_end_of_the_quarter
from raw_dates