import urllib.request
from urllib.parse import urlencode

from serve import running

params = urlencode({"title": "forest"})
with running(42082):
    url = "http://127.0.0.1:42082/search"
    with urllib.request.urlopen(url + "?" + params) as response:           # GET
        print("[client] GET :", response.read())
    with urllib.request.urlopen(url, data=params.encode()) as response:    # POST
        print("[client] POST:", response.read())
