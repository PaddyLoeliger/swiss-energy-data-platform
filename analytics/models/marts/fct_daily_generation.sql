{{ config(indexes=[{'columns': ['production_date'], 'unique': true}]) }}
with bounds as (
    select min(production_date) as first_day, max(production_date) as last_day
    from {{ ref('stg_electricity_production') }}
), calendar as (
    select generate_series(first_day::timestamp, last_day::timestamp, interval '1 day')::date as production_date
    from bounds
), expected as (
    select count(*) as expected_carriers from {{ ref('dim_energy_carrier') }}
), observed as (
    select s.production_date,
        count(*) as observed_carriers,
        count(d.energy_carrier) as known_carriers,
        count(*) filter (where not s.is_non_negative) as negative_values,
        sum(s.production_gwh) as reported_total_gwh
    from {{ ref('stg_electricity_production') }} s
    left join {{ ref('dim_energy_carrier') }} d using (energy_carrier)
    group by s.production_date
), classified as (
    select c.production_date, e.expected_carriers,
        coalesce(o.observed_carriers, 0) as observed_carriers,
        coalesce(o.known_carriers, 0) as known_carriers,
        coalesce(o.negative_values, 0) as negative_values,
        o.reported_total_gwh,
        coalesce(o.observed_carriers = e.expected_carriers and o.known_carriers = e.expected_carriers, false) as is_complete_day
    from calendar c cross join expected e
    left join observed o using (production_date)
)
select *, is_complete_day and negative_values = 0 as is_usable_day,
    case when is_complete_day and negative_values = 0 then reported_total_gwh end as usable_total_gwh
from classified
