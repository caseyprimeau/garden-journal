
-- Table: public.rainfall_test

-- DROP TABLE IF EXISTS public.rainfall_test;

CREATE TABLE IF NOT EXISTS public.rainfall_test
(
    id integer NOT NULL DEFAULT nextval('rainfall_test_id_seq'::regclass),
    datetime timestamp with time zone NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'::text),
    amount numeric(4,2),
    weather_json json,
    CONSTRAINT rainfall_test_pkey PRIMARY KEY (id)
)


--Returns the full dataset of rainfall data since collection began.
SELECT id
, datetime
, datetime AT TIME ZONE 'America/New_York' AS datetime_est
, amount
, weather_json
FROM public.rainfall_test
ORDER BY datetime_est DESC;

--Returns the total rainfall over the past week, compares to 25mm standard plant need
SELECT
SUM(amount) as weekly_total,
GREATEST((25 - SUM(amount)), 0) as water_needed
FROM public.rainfall_test
WHERE rainfall_test.datetime >= NOW() AT TIME ZONE 'UTC' - INTERVAL '7 day' 


--Returns the moving average of daily rainfall over the past week using CTE
WITH CTE_Filter As (
SELECT 
date_trunc('day', datetime) as datetime,
SUM(amount) as rainfill_mm
FROM public.rainfall_test
WHERE datetime >= NOW() AT TIME ZONE 'UTC' - INTERVAL '7 day' 
Group BY date_trunc('day', datetime)
)
SELECT
CONCAT(MIN (to_char(datetime, 'YYYY-MM-DD'))
,'-'
,MAX (to_char(datetime, 'YYYY-MM-DD'))) as date_range,
AVG(rainfill_mm)
From CTE_Filter



