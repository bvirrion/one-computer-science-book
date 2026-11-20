"""xss_demo.py -- stored cross-site scripting on the toy app: Eve posts a comment
with a script tag; Ada's browser fetches the page. Unsafe, then safe."""

import webapp
from client import Browser

for safe in (False, True):
    app, server = webapp.start(safe)
    eve, ada = Browser(), Browser()
    eve.request("/login", {"user": "eve", "password": "battery staple"})
    _, page = eve.request("/")
    token = page.split('name="csrf" value="')[1].split('"')[0] if safe else ""
    eve.request(
        "/comment", {"csrf": token, "text": "<script>alert(document.cookie)</script>"}
    )
    ada.request("/login", {"user": "ada", "password": "correct horse"})
    _, page = ada.request("/")
    print("safe" if safe else "unsafe", "app, the comment in Ada's page:")
    print("  " + page.splitlines()[1])
    print("  Ada's cookie flags:", ada.flags)
    server.shutdown()
    server.server_close()
