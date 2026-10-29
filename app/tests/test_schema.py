import os
import pytest

psycopg = pytest.importorskip("psycopg")
pytestmark = pytest.mark.skipif("PGHOST" not in os.environ, reason="no database configured")


def test_edge_requests_schema():
    with psycopg.connect() as conn:          # empty DSN = use the PG* environment variables
        cols = {r[0] for r in conn.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'edge_requests'")}
    assert {"ts", "pop", "status", "cache_status", "is_error"} <= cols
