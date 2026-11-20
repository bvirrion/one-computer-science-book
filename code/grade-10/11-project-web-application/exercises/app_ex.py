"""Exercises 3, 6, 7, 8, 11, 12 and 14: the application of milestone 5, extended."""
import sys
import threading
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
import app_m2  # noqa: E402
import app_m3  # noqa: E402
import app_m5  # noqa: E402
from app_m1 import dispatch as dispatch_m1  # noqa: E402
from data import BOOKS, MEMBERS  # noqa: E402

PER_PAGE = 20
LIMIT = 3  # reservations per member
LOCK = threading.Lock()


def about(request):  # exercise 3
    return app_m2.page("About", "<p>The Brenmoor library catalogue.</p>")


def author(request, name):  # exercise 6
    found = [n for n, b in sorted(BOOKS.items()) if b["author"] == name]
    if not found:
        return app_m2.not_found(request)
    items = "".join(f'<li><a href="/book/{n}">{escape(BOOKS[n]["title"])}</a></li>\n'
                    for n in found)
    return app_m2.page(f"Books by {name}", f"<ul>\n{items}</ul>")


def reserve_buggy(request):  # exercise 7: reads the URL instead of the form
    fake = dict(request, form=request["query"])
    return app_m3.reserve(fake)


def home(request):  # exercises 8 and 12: sorted, twenty books per page
    key = request["query"].get("sort", "title")
    if key not in ("title", "author", "year"):
        return app_m2.page("Bad sort", "<p>Sort by title, author or year.</p>", 400)
    page_text = request["query"].get("page", "1")
    pages = (len(BOOKS) + PER_PAGE - 1) // PER_PAGE
    if not page_text.isdigit() or not 1 <= int(page_text) <= pages:
        return app_m2.not_found(request)
    p = int(page_text)
    order = sorted(BOOKS, key=lambda n: (BOOKS[n][key], n))
    shown = order[(p - 1) * PER_PAGE:p * PER_PAGE]
    items = "".join(f'<li><a href="/book/{n}">{escape(BOOKS[n]["title"])}</a></li>\n'
                    for n in shown)
    nav = f"<p>page {p} of {pages}</p>"
    return app_m2.page("The Brenmoor library", f"<ul>\n{items}</ul>\n{nav}")


def reserve(request):  # exercise 14: at most LIMIT reservations per member
    member = request["form"].get("member", "")
    with LOCK:  # exercise 15: the check and the append happen together
        if member.isdigit() and int(member) in MEMBERS:
            held = sum(r.count(int(member)) for r in app_m3.RESERVATIONS.values())
            if held >= LIMIT:
                return app_m2.page("Limit reached", f"<p>{LIMIT} already.</p>", 409)
        return app_m3.reserve(request)


ROUTES = dict(app_m5.ROUTES)
ROUTES.update({"": (home, 0), "about": (about, 0), "author": (author, 1),
               "reserve": (reserve, 0)})
METHODS = {"reserve": {"POST"}}  # exercise 11: every other route takes GET only


def dispatch(request):
    first = request["path"].strip("/").split("/")[0]
    allowed = METHODS.get(first, {"GET"})
    if first in ROUTES and request["method"] not in allowed:
        allow = ", ".join(sorted(allowed))
        return app_m2.page("Method not allowed", "", 405, [("Allow", allow)])
    return dispatch_m1(request, ROUTES)
