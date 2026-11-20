import urllib.error
import urllib.request

from serve import running

with running(42081):
    for path in ["/hello", "/old-hello", "/no-such-page"]:
        try:
            with urllib.request.urlopen("http://127.0.0.1:42081" + path) as response:
                print("[client]", path, "->", response.status, "at", response.url)
        except urllib.error.HTTPError as error:
            print("[client]", path, "->", error.code, error.reason)
