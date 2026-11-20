"""Send one request and show the answer, without following redirects."""
import http.client
from urllib.parse import urlencode


def fetch(port, method, path, form=None, cookie=None):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    headers = {}
    body = None
    if form is not None:
        body = urlencode(form)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if cookie:
        headers["Cookie"] = cookie
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    text = response.read().decode("utf-8")
    connection.close()
    return response.status, dict(response.getheaders()), text


def show(port, method, path, form=None, cookie=None, lines=("<h1>",)):
    """Print the status, the interesting headers, and the body lines that match."""
    status, headers, text = fetch(port, method, path, form, cookie)
    print(f"{method} {path} -> {status}")
    for name in ("Location", "Set-Cookie", "Allow"):
        if name in headers:
            print(f"  {name}: {headers[name]}")
    for line in text.splitlines():
        if any(mark in line for mark in lines):
            print("  " + line)
    return status, headers, text
