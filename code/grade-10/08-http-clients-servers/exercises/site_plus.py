"""Exercises 11, 13 and 14: a sum route, server-side sessions, and a redirect loop."""
import secrets
import sys
from http.server import HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from library_site import Handler  # noqa: E402

SESSIONS = {}  # session id -> the data the server keeps for that visitor


class PlusHandler(Handler):
    def do_GET(self):
        url = urlsplit(self.path)
        params = parse_qs(url.query)
        if url.path == "/sum":
            try:
                total = int(params["a"][0]) + int(params["b"][0])
            except (KeyError, ValueError):
                self.reply(400, "need two whole numbers a and b\n")
                return
            self.reply(200, f"{total}\n")
        elif url.path == "/basket":
            self.basket(params.get("add", [None])[0])
        elif url.path == "/a":
            self.reply(302, "", extra=[("Location", "/b")])
        elif url.path == "/b":
            self.reply(302, "", extra=[("Location", "/a")])
        else:
            super().do_GET()

    def basket(self, item):
        cookie = self.headers.get("Cookie", "")
        sid = cookie.removeprefix("session=")
        extra = []
        if sid not in SESSIONS:
            sid = secrets.token_hex(8)
            SESSIONS[sid] = []
            extra.append(("Set-Cookie", f"session={sid}"))
        if item:
            SESSIONS[sid].append(item)
        self.reply(200, ", ".join(SESSIONS[sid]) + "\n", extra=extra)


def serve(port):
    return HTTPServer(("127.0.0.1", port), PlusHandler)
