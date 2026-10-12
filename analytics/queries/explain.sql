-- Broad aggregation: a sequential scan is often appropriate at this scale.
EXPLAIN (ANALYZE, BUFFERS)
SELECT energy_carrier, sum(production_gwh)
FROM analytics.fct_daily_generation_mix GROUP BY energy_carrier;

-- Selective date range: compare against the date-first compound index.
EXPLAIN (ANALYZE, BUFFERS)
SELECT production_date, energy_carrier, production_gwh
FROM analytics.fct_daily_generation_mix
WHERE production_date BETWEEN DATE '2025-01-01' AND DATE '2025-01-07';
