import urllib.request

from serve import running

with running(42080):
    request = urllib.request.Request("http://127.0.0.1:42080/hello",
                                     headers={"User-Agent": "brenmoor-client"})
    with urllib.request.urlopen(request) as response:
        print("[client] status:", response.status, response.reason)
        for name, value in response.getheaders():
            if name != "Date":  # changes every second
                print(f"[client] {name}: {value}")
        print("[client] body:", response.read())
