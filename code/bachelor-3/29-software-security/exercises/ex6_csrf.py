"""Exercise 6: a CSRF check for the toy web app. Every session gets a random token,
written into the app's own forms; a state-changing request is accepted only if its
form carries the token of the session its cookie names."""

import hmac
import secrets


def new_session(sessions, user):
    token = secrets.token_urlsafe(16)  # the session cookie's value
    sessions[token] = {"user": user, "csrf": secrets.token_urlsafe(16)}
    return token


def csrf_ok(sessions, cookie, form):
    s = sessions.get(cookie)
    sent = form.get("csrf", "")
    return s is not None and hmac.compare_digest(sent.encode(), s["csrf"].encode())


def require_csrf(handler):
    """Wrap a handler(app, user, form): refuse with 403 when the token is wrong."""

    def checked(app, cookie, form):
        if app.safe and not csrf_ok(app.sessions, cookie, form):
            return 403, "refused: missing or wrong CSRF token"
        return handler(app, cookie, form)

    return checked
