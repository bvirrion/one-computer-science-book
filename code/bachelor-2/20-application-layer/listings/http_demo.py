"""http_demo.py: one request by hand, then one connection per request or one for all."""
import http.client
import socket
import urllib.request

import http_server

http_server.serve(44201)
raw = socket.create_connection(("127.0.0.1", 44201))
raw.sendall(b"GET /library HTTP/1.1\r\nHost: www.brenmoor.test\r\n"
            b"Connection: close\r\n\r\n")
reply = b""
while (chunk := raw.recv(4096)):
    reply += chunk
print(reply.decode().replace("\r\n", "\n"), end="")

paths = ["/", "/library", "/harbour", "/", "/library"] * 4
http_server.stats.update(connections=0, requests=0)
for p in paths:                                  # urllib asks to close each time
    urllib.request.urlopen(f"http://127.0.0.1:44201{p}").read()
print("\nurllib:     ", http_server.stats)
http_server.stats.update(connections=0, requests=0)
conn = http.client.HTTPConnection("127.0.0.1", 44201)
for p in paths:                                  # one persistent connection
    conn.request("GET", p)
    conn.getresponse().read()
print("http.client:", http_server.stats)
