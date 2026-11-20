import http.cookiejar
import urllib.request

from serve import running

jar = http.cookiejar.CookieJar()
browser = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
with running(42083):
    for _ in range(3):
        with browser.open("http://127.0.0.1:42083/count") as response:
            cookie = response.headers["Set-Cookie"]
            print("[client]", response.read(), "Set-Cookie:", cookie)
    print("[client] the jar holds:", [(c.name, c.value) for c in jar])
