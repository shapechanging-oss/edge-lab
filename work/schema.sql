BEGIN;
DROP TABLE IF EXISTS edge_requests;
CREATE TABLE edge_requests (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ts           timestamptz NOT NULL,
  pop          text        NOT NULL,
  client_ip    inet,
  path         text,
  status       smallint    NOT NULL,
  bytes        bigint      NOT NULL DEFAULT 0,
  cache_status text        NOT NULL CHECK (cache_status IN ('HIT','MISS','STALE')),
  ttfb_ms      integer,
  headers      jsonb
);
-- CREATE TABLE ... (step 2)
-- INSERT ... (step 3)
INSERT INTO edge_requests (ts, pop, client_ip, path, status, bytes, cache_status, ttfb_ms)
SELECT now() - random() * interval '2 hours',
       (ARRAY['bos','fra','sin','gru'])[1 + floor(random() * 4)::int],
       ('10.0.' || floor(random() * 255) || '.' || floor(random() * 255))::inet,
       '/img/' || floor(random() * 500) || '.jpg',
       CASE WHEN random() < 0.01 THEN 503 ELSE 200 END,
       floor(random() * 500000),
       (ARRAY['HIT','HIT','HIT','MISS','STALE'])[1 + floor(random() * 5)::int],
       floor(random() * random() * 800)
FROM generate_series(1, 1000000);

COMMIT;
ANALYZE edge_requests;
