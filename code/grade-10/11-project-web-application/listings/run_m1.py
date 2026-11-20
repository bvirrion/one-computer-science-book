import app_m1
from client import fetch
from server import start

server = start(app_m1, 42111)
for path in ["/", "/book/7", "/book/999", "/book/seven", "/book", "/shop"]:
    status, headers, text = fetch(42111, "GET", path)
    print(f"{path:12} {status}  {text.strip()}")
server.shutdown()
