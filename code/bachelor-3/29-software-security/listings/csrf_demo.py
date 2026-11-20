"""csrf_demo.py -- cross-site request forgery on the toy app: Ada is logged in, and
a page on another site makes her browser post to /renew. Her browser adds her
session cookie by itself. Unsafe, then safe."""

import webapp
from client import Browser

for safe in (False, True):
    app, server = webapp.start(safe)
    ada = Browser()
    ada.request("/login", {"user": "ada", "password": "correct horse"})
    # The forged form: the other site knows the route and fields, not the token
    status, body = ada.request("/renew", {"weeks": "52"})
    print("safe" if safe else "unsafe", "app, forged request:", status, body)
    _, page = ada.request("/")  # Ada's own form carries the token
    token = page.split('name="csrf" value="')[1].split('"')[0] if safe else ""
    status, body = ada.request("/renew", {"weeks": "2", "csrf": token})
    print("   Ada's own request:", status, body)
    server.shutdown()
    server.server_close()
