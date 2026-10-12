{{ config(indexes=[{'columns': ['production_date', 'energy_carrier'], 'unique': true}]) }}
select f.production_date, d.energy_carrier, d.carrier_label,
    s.production_gwh,
    s.run_id,
    s.quality_flag,
    s.production_date is not null as is_observed,
    f.is_complete_day, f.is_usable_day,
    case when f.is_usable_day and f.usable_total_gwh > 0
        then s.production_gwh / f.usable_total_gwh end as generation_share
from {{ ref('fct_daily_generation') }} f
cross join {{ ref('dim_energy_carrier') }} d
left join {{ ref('stg_electricity_production') }} s
    on s.production_date = f.production_date and s.energy_carrier = d.energy_carrier
