"""dns_demo.py: the brenmoor.test server on UDP port 44200, and queries to it."""
import socket

from dns_message import decode, query
from resolve import text
from zone import BRENMOOR, serve_udp

serve_udp(BRENMOOR, 44200)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(2)
for i, (name, rtype) in enumerate([("www.brenmoor.test", "A"),
                                   ("www.brenmoor.test", "AAAA"),
                                   ("brenmoor.test", "MX"), ("brenmoor.test", "TXT"),
                                   ("nowhere.brenmoor.test", "A")]):
    q = query(100 + i, name, rtype)
    client.sendto(q, ("127.0.0.1", 44200))
    data, _ = client.recvfrom(512)               # one datagram each way
    reply = decode(data)
    found = ", ".join(text(r[3]) for r in reply["answer"]) or "none"
    code = {0: "ok", 3: "no such name"}[reply["flags"] & 0xF]
    print(f"{name:22} {rtype:5} {len(q):3} -> {len(data):3} bytes  {code:12} {found}")
