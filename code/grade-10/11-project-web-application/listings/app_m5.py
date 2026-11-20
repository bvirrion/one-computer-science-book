"""Milestone 5: a cookie that remembers the last search, and a JSON route."""
import json
from html import escape
from urllib.parse import quote, unquote

import app_m2
import app_m3
from app_m1 import dispatch as dispatch_m1
from app_m1 import reply
from data import BOOKS, LOANS


def search(request):
    status, kind, text, headers = app_m3.search(request)
    words = request["query"].get("q", "").strip()
    headers.append(("Set-Cookie", f"last={quote(words)}; Path=/; HttpOnly"))
    return status, kind, text, headers


def home(request):
    status, kind, text, headers = app_m2.home(request)
    last = unquote(request["cookies"].get("last", ""))
    if last:
        link = f'<a href="/search?q={quote(last)}">{escape(last)}</a>'
        text = text.replace("<ul>", f"<p>Your last search: {link}</p>\n<ul>", 1)
    return status, kind, text, headers


def api(request, kind, number):
    if kind != "book" or not number.isdigit() or int(number) not in BOOKS:
        error = json.dumps({"error": "no such book"})
        return reply(404, error + "\n", "application/json")
    n = int(number)
    b = BOOKS[n]
    record = {"book": n, "title": b["title"], "author": b["author"],
              "year": int(b["year"]), "loans": len(LOANS.get(n, [])),
              "reserved_by": app_m3.RESERVATIONS.get(n, [])}
    return reply(200, json.dumps(record, indent=1) + "\n", "application/json")


ROUTES = dict(app_m3.ROUTES)
ROUTES.update({"": (home, 0), "search": (search, 0), "api": (api, 2)})


def dispatch(request):
    return dispatch_m1(request, ROUTES)
