-- expects: -v pop=<code>
SELECT date_trunc('minute', ts) AS minute,
       count(*) AS requests,
       round(100.0 * count(*) FILTER (WHERE cache_status = 'HIT') / count(*), 1) AS hit_pct
FROM edge_requests
WHERE pop = :'pop'
  AND ts >= now() - interval '1 hour'
GROUP BY 1
ORDER BY 1;
