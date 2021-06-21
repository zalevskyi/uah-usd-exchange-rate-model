CREATE TABLE data_for_model AS
SELECT quote_date,
       uah_usd,
       round(uah_usd/uah_eur,4) as eur_usd,
       round(uah_usd/uah_rub,4) as rub_usd,
       round(uah_usd/uah_pln,4) as pln_usd,
       brent,
       steal,
       wheat,
       mvemsd
FROM data
WHERE uah_usd IS NOT NULL
      AND eur_usd IS NOT NULL
      AND rub_usd IS NOT NULL
      AND pln_usd IS NOT NULL
      AND brent IS NOT NULL
      AND steal IS NOT NULL
      AND mvemsd IS NOT NULL;