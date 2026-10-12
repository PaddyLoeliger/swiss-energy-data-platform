select current_date as checked_on,
    min(production_date) as first_source_date,
    max(production_date) as latest_source_date,
    current_date - max(production_date) as source_age_days,
    count(*) as calendar_days,
    count(*) filter (where not is_complete_day) as incomplete_days,
    count(*) filter (where negative_values > 0) as negative_value_days,
    coalesce(max(production_date) >= current_date - {{ var('max_source_age_days') }}, false) as within_freshness_target
from {{ ref('fct_daily_generation') }}
