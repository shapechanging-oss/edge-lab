"""Tiny origin service for the edge lab."""
import functools, json, os, signal, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            return self._json(200, {"status": "ok", "version": VERSION})
        if self.path == "/ready":
            return self._json(200, {"ready": True})
        return super().do_GET()

    def _json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")     # health checks must never be cached
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def make_server(port=5000, directory="static"):
    handler = functools.partial(Handler, directory=directory)
    return ThreadingHTTPServer(("0.0.0.0", port), handler)


if __name__ == "__main__":
    srv = make_server(int(os.environ.get("PORT", "5000")))
    # As PID 1 in a container, SIGTERM is ignored unless we handle it (Chapter 1.1).
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=srv.shutdown).start())
    print(f"listening on :{srv.server_address[1]}", flush=True)
    srv.serve_forever()
