"""Problem: what one page of the library site costs: requests, bytes, round trips."""
import sys
import threading
import urllib.request
from html.parser import HTMLParser
from http.server import HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from library_site import Handler  # noqa: E402

PORT = 42090
LATENCY_MS = 50


class Resources(HTMLParser):
    """Collect the addresses of the stylesheets and images a page asks for."""

    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "stylesheet":
            self.found.append(a["href"])
        elif tag == "img":
            self.found.append(a["src"])


class Quiet(Handler):
    def log_request(self, code="-", size="-"):
        pass


def fetch_page(port=PORT):
    """Return the list of (path, bytes of the body) for the page and its resources."""
    server = HTTPServer(("127.0.0.1", port), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        base = f"http://127.0.0.1:{port}/"
        with urllib.request.urlopen(base + "page.html") as r:
            html = r.read()
        got = [("page.html", len(html))]
        parser = Resources()
        parser.feed(html.decode("utf-8"))
        for path in parser.found:
            with urllib.request.urlopen(base + path) as r:
                got.append((path, len(r.read())))
        return got
    finally:
        server.shutdown()
        server.server_close()


def round_trips(requests, reuse):
    """One round trip to open a connection, one per request and response."""
    return (1 + requests) if reuse else 2 * requests


if __name__ == "__main__":
    got = fetch_page()
    for path, size in got:
        print(f"{path:10} {size:4} bytes")
    n = len(got)
    print(n, "requests,", sum(s for _, s in got), "bytes of content")
    for reuse in (False, True):
        rt = round_trips(n, reuse)
        ms = rt * LATENCY_MS
        print(f"reuse={reuse}: {rt} round trips = {ms} ms at {LATENCY_MS} ms")
