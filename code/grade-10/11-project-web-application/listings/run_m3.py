import app_m3
from client import show
from server import start

server = start(app_m3, 42113)
show(42113, "GET", "/search?q=forest", lines=("<h1>", "found", "<li>"))
show(42113, "GET", "/search?q=%3Cb%3Ehi", lines=("<h1>",))
show(42113, "POST", "/reserve", form={"book": "7", "member": "12"})
show(42113, "POST", "/reserve", form={"book": "7", "member": "99"})
show(42113, "GET", "/book/7", lines=("Reserved by",))
server.shutdown()
