#!/usr/bin/env python3
"""Per-minute cache hit ratio for one POP, written as CSV to stdout."""
import argparse, csv, logging, random, sys, time
import psycopg

SQL = """
SELECT date_trunc('minute', ts) AS minute,
       count(*) AS requests,
       round(100.0 * count(*) FILTER (WHERE cache_status = 'HIT') / count(*), 1) AS hit_pct
FROM edge_requests
WHERE pop = %(pop)s
  AND ts >= now() - make_interval(mins => %(minutes)s)
GROUP BY 1 ORDER BY 1
"""
log = logging.getLogger("pop_report")


def connect_with_retry(dsn: str, attempts: int = 5) -> psycopg.Connection:
    delay = 1.0
    for attempt in range(1, attempts + 1):
        try:
            return psycopg.connect(
                dsn, connect_timeout=5,
                options="-c statement_timeout=30s -c default_transaction_read_only=on")
        except psycopg.OperationalError as e:
            if attempt == attempts:
                raise
            sleep = delay + random.uniform(0, delay)          # backoff with jitter
            log.warning("connect %d/%d failed (%s); retrying in %.1fs", attempt, attempts, e, sleep)
            time.sleep(sleep)
            delay *= 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pop")
    ap.add_argument("--minutes", type=int, default=60)
    ap.add_argument("--dsn", default="service=edge_rw")
    ap.add_argument("--dry-run", action="store_true", help="print the SQL and plan; fetch nothing")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(asctime)s %(levelname)s %(message)s")

    params = {"pop": args.pop, "minutes": args.minutes}
    with connect_with_retry(args.dsn) as conn:
        if args.dry_run:
            cur = psycopg.ClientCursor(conn)
            print(cur.mogrify(SQL, params), file=sys.stderr)      # the exact SQL that would run
            for (line,) in cur.execute("EXPLAIN " + SQL, params):
                print(line, file=sys.stderr)
            return 0
        cur = conn.execute(SQL, params)
        out = csv.writer(sys.stdout)
        out.writerow([c.name for c in cur.description])
        out.writerows(cur)
    return 0


if __name__ == "__main__":
    sys.exit(main())
