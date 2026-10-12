{{ config(severity='warn') }}
select * from {{ ref('fct_daily_generation') }} where not is_usable_day
