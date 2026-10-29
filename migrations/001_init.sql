CREATE TABLE IF NOT EXISTS edge_requests (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ts           timestamptz NOT NULL,
  pop          text        NOT NULL,
  client_ip    inet,
  path         text,
  status       smallint    NOT NULL,
  bytes        bigint      NOT NULL DEFAULT 0,
  cache_status text        NOT NULL CHECK (cache_status IN ('HIT','MISS','STALE')),
  ttfb_ms      integer,
  headers      jsonb,
  is_error     boolean
);
CREATE INDEX IF NOT EXISTS edge_requests_pop_ts ON edge_requests (pop, ts);
