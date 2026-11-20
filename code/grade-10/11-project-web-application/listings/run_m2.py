import app_m2
from client import fetch, show
from server import start

server = start(app_m2, 42112)
show(42112, "GET", "/", lines=("<h1>", "/book/7\""))
status, headers, text = fetch(42112, "GET", "/book/7")
print("GET /book/7 ->", status, headers["Content-Type"])
print(text, end="")
show(42112, "GET", "/<script>alert('hello')</script>", lines=("error",))
server.shutdown()
