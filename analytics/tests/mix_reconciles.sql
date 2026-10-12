select production_date
from {{ ref('fct_daily_generation_mix') }}
group by production_date
having count(*) <> (select count(*) from {{ ref('dim_energy_carrier') }})
    or (count(generation_share) > 0 and abs(sum(generation_share) - 1) > 0.000000001)
    or bool_or(generation_share < 0 or generation_share > 1)
    or bool_or(not is_usable_day and generation_share is not null)
