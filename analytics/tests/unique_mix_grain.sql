select production_date, energy_carrier
from {{ ref('fct_daily_generation_mix') }}
group by 1, 2 having count(*) <> 1
