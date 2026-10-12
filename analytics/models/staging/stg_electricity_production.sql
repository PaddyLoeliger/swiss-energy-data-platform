select
    production_date,
    energy_carrier,
    production_gwh,
    run_id,
    quality_flag,
    production_gwh >= 0 as is_non_negative
from {{ source('energy_raw', 'electricity_production') }}
