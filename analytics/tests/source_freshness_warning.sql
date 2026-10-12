{{ config(severity='warn') }}
select * from {{ ref('energy_quality_status') }} where not within_freshness_target
