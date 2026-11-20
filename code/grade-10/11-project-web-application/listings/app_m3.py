"""Milestone 3: a search form (GET) and a reservation form (POST, then a redirect)."""
from html import escape

import app_m2
from app_m1 import dispatch as dispatch_m1
from data import BOOKS, MEMBERS

RESERVATIONS = {}  # book number -> member numbers, kept in memory only
SEARCH_FORM = ('<form action="/search" method="get">'
               '<input name="q"> <button>Search</button></form>')


def search(request):
    words = request["query"].get("q", "").strip()
    found = [n for n, b in sorted(BOOKS.items())
             if words and words.lower() in b["title"].lower()]
    items = "".join(f'<li><a href="/book/{n}">{escape(BOOKS[n]["title"])}</a></li>\n'
                    for n in found)
    body = f"{SEARCH_FORM}\n<p>{len(found)} found</p>\n<ul>\n{items}</ul>"
    return app_m2.page(f"Search: {words}", body)


def book(request, number):
    if not number.isdigit() or int(number) not in BOOKS:
        return app_m2.not_found(request)
    n = int(number)
    who = ", ".join(str(m) for m in RESERVATIONS.get(n, [])) or "nobody"
    form = (f'<form action="/reserve" method="post">'
            f'<input type="hidden" name="book" value="{n}">'
            f'Member number: <input name="member"> <button>Reserve</button></form>')
    body = f"{app_m2.book_body(n)}\n<p>Reserved by: {who}</p>\n{form}"
    return app_m2.page(BOOKS[n]["title"], body)


def reserve(request):
    book_n, member = request["form"].get("book", ""), request["form"].get("member", "")
    if not (book_n.isdigit() and int(book_n) in BOOKS):
        return app_m2.page("No such book", "<p>Choose a book first.</p>", 400)
    if not (member.isdigit() and int(member) in MEMBERS):
        return app_m2.page("No such member", f"<p>{escape(member)}?</p>", 400)
    RESERVATIONS.setdefault(int(book_n), []).append(int(member))
    return app_m2.page("Reserved", "", 303, [("Location", f"/book/{book_n}")])


ROUTES = dict(app_m2.ROUTES)
ROUTES.update({"book": (book, 1), "search": (search, 0), "reserve": (reserve, 0)})


def dispatch(request):
    return dispatch_m1(request, ROUTES)
