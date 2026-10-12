{{ config(indexes=[{'columns': ['production_date'], 'unique': true}]) }}
with windows as (
    select production_date,
        count(*) over rolling_window as calendar_days_7d,
        count(usable_total_gwh) over rolling_window as usable_days_7d,
        avg(usable_total_gwh) over rolling_window as candidate_average
    from {{ ref('fct_daily_generation') }}
    window rolling_window as (order by production_date rows between 6 preceding and current row)
)
select production_date, calendar_days_7d, usable_days_7d,
    case when calendar_days_7d = 7 and usable_days_7d = 7 then candidate_average end as average_daily_gwh_7d
from windows
