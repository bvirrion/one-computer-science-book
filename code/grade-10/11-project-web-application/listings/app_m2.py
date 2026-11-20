"""Milestone 2: HTML pages built from the tables, with every value escaped."""
from html import escape

from app_m1 import dispatch as dispatch_m1
from app_m1 import reply
from data import BOOKS, HERE, LOANS


def page(title, body, status=200, headers=()):
    html = ('<!DOCTYPE html>\n<html><head><meta charset="utf-8">\n'
            f"<title>{escape(title)}</title>\n"
            '<link rel="stylesheet" href="/style.css"></head>\n'
            f"<body>\n<h1>{escape(title)}</h1>\n{body}\n</body></html>\n")
    return reply(status, html, "text/html", headers)


def home(request):
    items = [f'<li><a href="/book/{n}">{escape(b["title"])}</a></li>'
             for n, b in sorted(BOOKS.items())]
    return page("The Brenmoor library", "<ul>\n" + "\n".join(items) + "\n</ul>")


def book_body(n):
    b = BOOKS[n]
    rows = [f"<tr><td>{escape(loan['out_date'])}</td>"
            f"<td>{escape(loan['return_date'] or 'not yet')}</td></tr>\n"
            for loan in LOANS.get(n, [])]
    return (f"<p>{escape(b['author'])}, {b['year']}, {b['pages']} pages</p>\n"
            "<table>\n<tr><th>out</th><th>back</th></tr>\n"
            f"{''.join(rows)}</table>")


def book(request, number):
    if not number.isdigit() or int(number) not in BOOKS:
        return not_found(request)
    return page(BOOKS[int(number)]["title"], book_body(int(number)))


def not_found(request):
    text = f'<p class="error">No page at {escape(request["path"])}</p>'
    return page("Not found", text, status=404)


def style(request):
    return reply(200, (HERE / "style.css").read_text(), "text/css")


ROUTES = {"": (home, 0), "book": (book, 1), "style.css": (style, 0),
          None: (not_found, 0)}


def dispatch(request):
    return dispatch_m1(request, ROUTES)
