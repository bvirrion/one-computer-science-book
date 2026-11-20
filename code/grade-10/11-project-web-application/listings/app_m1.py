"""Milestone 1: routes and a dispatcher. The pages are plain text for now."""
from data import BOOKS


def reply(status, text, kind="text/plain", headers=()):
    return status, kind, text, list(headers)


def home(request):
    return reply(200, f"The library has {len(BOOKS)} books.\n")


def book(request, number):
    if not number.isdigit() or int(number) not in BOOKS:
        return not_found(request)
    b = BOOKS[int(number)]
    return reply(200, f"{b['title']}, by {b['author']} ({b['year']})\n")


def not_found(request):
    return reply(404, f"No page at {request['path']}\n")


# first part of the path -> (function, number of further parts it takes)
ROUTES = {"": (home, 0), "book": (book, 1), None: (not_found, 0)}


def dispatch(request, routes=ROUTES):
    """Choose the function by the first part of the path; the others are arguments."""
    first, *rest = request["path"].strip("/").split("/")
    function, count = routes.get(first, routes[None])
    if len(rest) != count:
        function, rest = routes[None][0], []
    return function(request, *rest)
