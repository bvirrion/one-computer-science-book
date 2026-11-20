"""client.py -- a tiny browser for the demos: it keeps the session cookie and sends
it with every request to the app, as a browser does."""

import urllib.error
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:45291"


class Browser:
    def __init__(self):
        self.cookie = None

    def request(self, path, form=None):
        data = urllib.parse.urlencode(form).encode() if form is not None else None
        req = urllib.request.Request(BASE + path, data=data)
        if self.cookie:
            req.add_header("Cookie", f"session={self.cookie}")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                status, body, headers = r.status, r.read().decode(), r.headers
        except urllib.error.HTTPError as e:
            status, body, headers = e.code, e.read().decode(), e.headers
        set_cookie = headers.get("Set-Cookie")
        if set_cookie:
            self.cookie = set_cookie.split(";")[0].split("=", 1)[1]
            self.flags = set_cookie.split(";")[1:]
        return status, body
