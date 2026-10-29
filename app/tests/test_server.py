import json
import threading
import urllib.request
import pytest
from src.server import make_server


@pytest.fixture
def base_url(tmp_path):
    (tmp_path / "index.html").write_text("hello edge")
    srv = make_server(0, directory=str(tmp_path))      # port 0 = any free port
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def test_health(base_url):
    with urllib.request.urlopen(f"{base_url}/health") as r:
        assert r.status == 200
        assert json.load(r)["status"] == "ok"


def test_static_file(base_url):
    with urllib.request.urlopen(f"{base_url}/index.html") as r:
        assert r.read() == b"hello edge"
