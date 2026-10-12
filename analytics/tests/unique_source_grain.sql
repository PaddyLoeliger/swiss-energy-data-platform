select production_date, energy_carrier
from {{ ref('stg_electricity_production') }}
group by 1, 2 having count(*) <> 1
