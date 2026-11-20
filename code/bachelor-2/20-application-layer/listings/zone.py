"""zone.py: authoritative name servers for the root, test and brenmoor.test."""
import socket
import threading

from dns_message import AA, QR, decode, encode

NXDOMAIN = 3


def inside(name, zone):
    return zone == "" or name == zone or name.endswith("." + zone)


class Server:
    def __init__(self, origin, records):
        self.origin, self.records = origin, records

    def answer(self, data):
        q = decode(data)
        name, rtype = q["question"][0]
        name = name.lower()
        reply = {"id": q["id"], "flags": QR, "question": q["question"],
                 "answer": [], "authority": [], "additional": []}
        for cut in self.find(None, "NS"):        # a delegation below this zone?
            if cut[0] != self.origin and inside(name, cut[0]):
                reply["authority"] = self.find(cut[0], "NS")
                reply["additional"] = [g for ns in reply["authority"]
                                       for g in self.find(ns[3], "A")]
                return encode(reply)             # a referral: ask them instead
        reply["flags"] |= AA                     # the answer is ours to give
        while not self.find(name, rtype) and self.find(name, "CNAME"):
            alias = self.find(name, "CNAME")[0]
            reply["answer"].append(alias)
            name = alias[3]                      # follow the alias in this zone
        reply["answer"] += self.find(name, rtype)
        if not any(r[0] == name for r in self.records):
            reply["flags"] |= NXDOMAIN           # no such name at all
        return encode(reply)

    def find(self, name, rtype):
        return [r for r in self.records if r[1] == rtype and name in (None, r[0])]


ROOT = Server("", [("test", "NS", 172800, "ns.test"),
                   ("ns.test", "A", 172800, "198.51.100.53")])
TEST = Server("test", [("test", "NS", 172800, "ns.test"),
                       ("brenmoor.test", "NS", 86400, "ns.brenmoor.test"),
                       ("ns.brenmoor.test", "A", 86400, "203.0.113.53")])
BRENMOOR = Server("brenmoor.test", [
    ("brenmoor.test", "NS", 86400, "ns.brenmoor.test"),
    ("brenmoor.test", "MX", 3600, (10, "mail.brenmoor.test")),
    ("brenmoor.test", "TXT", 3600, "Brenmoor town hall"),
    ("ns.brenmoor.test", "A", 86400, "203.0.113.53"),
    ("www.brenmoor.test", "A", 3600, "127.0.0.1"),     # this machine, for the demos
    ("www.brenmoor.test", "AAAA", 3600, "2001:db8::80"),
    ("mail.brenmoor.test", "A", 3600, "192.0.2.25"),
    ("library.brenmoor.test", "CNAME", 3600, "www.brenmoor.test")])

# the toy Internet of the resolution examples: address -> server
NETWORK = {"192.0.2.53": ROOT, "198.51.100.53": TEST, "203.0.113.53": BRENMOOR}


def serve_udp(server, port):
    """Answer queries on 127.0.0.1:port in a background thread."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))

    def loop():
        while True:
            data, client = sock.recvfrom(512)
            sock.sendto(server.answer(data), client)
    threading.Thread(target=loop, daemon=True).start()
    return sock
