select * from {{ ref('fct_generation_rolling') }}
where (average_daily_gwh_7d is not null) <> (calendar_days_7d = 7 and usable_days_7d = 7)
