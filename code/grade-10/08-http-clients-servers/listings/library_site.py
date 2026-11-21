import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

FILES = Path(__file__).parent / "site_files"
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css",
         ".svg": "image/svg+xml"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def version_string(self):
        return "BrenmoorSite/1.0"

    def log_request(self, code="-", size="-"):
        print(f"[server] {self.requestline} -> {code}", flush=True)

    def reply(self, status, body, kind="text/plain; charset=utf-8", extra=()):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        for name, value in extra:
            self.send_header(name, value)
        self.end_headers()           # the blank line
        self.wfile.write(data)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/hello":
            self.reply(200, "Hello from Brenmoor\n")
        elif url.path == "/old-hello":
            self.reply(303, "", extra=[("Location", "/hello")])
        elif url.path == "/search":
            self.search(parse_qs(url.query))
        elif url.path == "/count":
            self.count()
        elif ".." not in url.path and (FILES / url.path.lstrip("/")).is_file():
            file = FILES / url.path.lstrip("/")
            self.reply(200, file.read_bytes(), TYPES[file.suffix])
        else:
            self.reply(404, "No such page\n")

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")
        print(f"[server] body: {body}", flush=True)
        if self.path == "/search":
            self.search(parse_qs(body))
        else:
            self.reply(404, "No such page\n")

    def search(self, params):
        title = params.get("title", [""])[0]
        self.reply(200, f"Searching for {title!r}\n")

    def count(self):
        cookie = self.headers.get("Cookie", "")
        visits = int(cookie.removeprefix("visits=") or 0) + 1
        self.reply(200, f"Visit number {visits}\n",
                   extra=[("Set-Cookie", f"visits={visits}")])


if __name__ == "__main__":
    port = int(sys.argv[1])
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
