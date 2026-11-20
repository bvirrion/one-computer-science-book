"""visit.py: what happens when a browser opens http://www.brenmoor.test/."""
import http.client
import socket

import http_server
from dns_message import decode, query
from zone import BRENMOOR, serve_udp

serve_udp(BRENMOOR, 44202)                       # the town's name server
http_server.serve(44203)                         # the town's web server

print("looking up www.brenmoor.test ...", end=" ")
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(query(1, "www.brenmoor.test", "A"), ("127.0.0.1", 44202))
address = decode(udp.recv(512))["answer"][0][3]
print(address)
print(f"connecting to {address} port 44203 ...", end=" ")
conn = http.client.HTTPConnection(address, 44203)
conn.connect()
print("connected")
conn.request("GET", "/", headers={"Host": "www.brenmoor.test"})
reply = conn.getresponse()
page = reply.read()
print(f"GET / ... {reply.status} {reply.reason}, {len(page)} bytes of "
      f"{reply.getheader('Content-Type')}")
print(page.decode(), end="")
