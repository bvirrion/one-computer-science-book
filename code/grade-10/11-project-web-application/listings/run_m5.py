import app_m5
from client import show
from server import start

server = start(app_m5, 42115)
_, headers, _ = show(42115, "GET", "/search?q=silent%20forest", lines=("found",))
cookie = headers["Set-Cookie"].split(";")[0]  # what the browser keeps: name=value
show(42115, "GET", "/", cookie=cookie, lines=("last search",))
show(42115, "POST", "/reserve", form={"book": "7", "member": "12"})
status, headers, text = show(42115, "GET", "/api/book/7", lines=())
print(headers["Content-Type"])
print(text, end="")
show(42115, "GET", "/api/book/700", lines=("error",))
server.shutdown()
