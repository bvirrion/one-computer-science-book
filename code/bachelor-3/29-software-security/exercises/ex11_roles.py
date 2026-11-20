"""Exercise 11: least-privilege roles for the toy app, as an access-control matrix
of roles by routes; every route checks the matrix before it runs."""

ROUTES = [
    "view_page",
    "post_comment",
    "renew_own_loan",
    "renew_any_loan",
    "delete_comment",
    "export_loans",
    "manage_users",
]
ROLES = {
    "visitor": {"view_page"},
    "reader": {"view_page", "post_comment", "renew_own_loan"},
    "librarian": {
        "view_page",
        "post_comment",
        "renew_own_loan",
        "renew_any_loan",
        "delete_comment",
        "export_loans",
    },
    "admin": {"view_page", "manage_users"},  # administers accounts, not loans
}


def allowed(role, route):
    return route in ROLES.get(role, set())  # deny anything not granted


def matrix():
    return {role: [allowed(role, r) for r in ROUTES] for role in ROLES}
