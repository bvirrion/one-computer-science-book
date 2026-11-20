"""webapp.py -- the library's toy web app (stdlib http.server, on 127.0.0.1 only).
Readers log in, post comments and renew loans. With safe=False it has the classic
bugs; with safe=True each one is fixed: comments are escaped, state-changing forms
need a CSRF token, and the session cookie gets the HttpOnly and SameSite flags."""

import html
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from ex6_csrf import new_session, require_csrf  # noqa: E402

PASSWORDS = {"ada": "correct horse", "eve": "battery staple"}  # invented test accounts


class App:
    def __init__(self, safe):
        self.safe, self.sessions, self.comments, self.loans = safe, {}, [], {}

    def page(self, cookie):
        s = self.sessions.get(cookie)
        show = html.escape if self.safe else (lambda text: text)  # the escape point
        items = "".join(
            f"<li>{show(who)}: {show(text)}</li>\n" for who, text in self.comments
        )
        token = f'<input type="hidden" name="csrf" value="{s["csrf"]}">' if s else ""
        form = (
            f'<form method="post" action="/comment">{token}<input name="text"></form>'
        )
        return 200, f"<ul>\n{items}</ul>\n{form}"

    def login(self, form):
        if PASSWORDS.get(form.get("user")) != form.get("password"):
            return 403, "wrong name or password", None
        return 200, "welcome", new_session(self.sessions, form["user"])

    @require_csrf
    def comment(self, cookie, form):
        s = self.sessions.get(cookie)
        if not s:
            return 403, "log in first"
        self.comments.append((s["user"], form.get("text", "")))
        return 200, "comment posted"

    @require_csrf
    def renew(self, cookie, form):
        s = self.sessions.get(cookie)
        if not s:
            return 403, "log in first"
        self.loans[s["user"]] = form.get("weeks", "1")
        return 200, f"loan of {s['user']} renewed for {self.loans[s['user']]} weeks"


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # keep the demos' output quiet
            pass

        def cookie(self):
            raw = self.headers.get("Cookie", "")
            return dict(
                p.strip().split("=", 1) for p in raw.split(";") if "=" in p
            ).get("session")

        def reply(self, status, body, session=None):
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            if session:
                flags = "; HttpOnly; SameSite=Strict" if app.safe else ""
                self.send_header("Set-Cookie", f"session={session}{flags}")
            self.end_headers()
            self.wfile.write(body.encode())

        def do_GET(self):
            self.reply(*app.page(self.cookie()))

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            form = dict(urllib.parse.parse_qsl(self.rfile.read(n).decode()))
            if self.path == "/login":
                self.reply(*app.login(form))
            elif self.path == "/comment":
                self.reply(*app.comment(self.cookie(), form))
            elif self.path == "/renew":
                self.reply(*app.renew(self.cookie(), form))
            else:
                self.reply(404, "no such page")

    return Handler


def start(safe, port=45291):
    app = App(safe)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(app))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return app, server
