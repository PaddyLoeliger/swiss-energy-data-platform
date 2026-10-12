select 1 where not exists (select 1 from {{ source('energy_raw', 'electricity_production') }})
