"""Serve an application module on 127.0.0.1: python server.py app_m3 42110."""
import importlib
import sys
import threading
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit


def make_handler(app):
    class Handler(BaseHTTPRequestHandler):
        def answer(self):
            url = urlsplit(self.path)
            size = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(size).decode("utf-8")
            cookies = SimpleCookie(self.headers.get("Cookie", ""))
            request = {
                "method": self.command,
                "path": unquote(url.path),
                "query": {k: v[0] for k, v in parse_qs(url.query).items()},
                "form": {k: v[0] for k, v in parse_qs(body).items()},
                "cookies": {k: m.value for k, m in cookies.items()},
            }
            status, kind, text, headers = app.dispatch(request)
            data = text.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            for name, value in headers:
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(data)

        do_GET = do_POST = do_PUT = do_DELETE = answer

        def log_message(self, *args):  # keep the terminal quiet
            pass

    return Handler


def start(app, port):
    """Serve `app` in a background thread; call .shutdown() on the result to stop."""
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(app))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    app = importlib.import_module(sys.argv[1])
    port = int(sys.argv[2])
    print(f"serving {sys.argv[1]} on http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), make_handler(app)).serve_forever()
