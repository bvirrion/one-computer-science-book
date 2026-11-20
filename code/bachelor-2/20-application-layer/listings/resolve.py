"""resolve.py: iterative resolution, from the root down, in the wire format."""
import itertools

from dns_message import decode, query
from zone import NETWORK, NXDOMAIN

ROOT_ADDRESS = "192.0.2.53"
ids = itertools.count(1)


def resolve(name, rtype, send, show=print):
    """Ask the root, then follow referrals; return (records, queries sent)."""
    server, sent = ROOT_ADDRESS, 0
    while True:
        show(f"ask {server:14} {name} {rtype}")
        reply = decode(send(server, query(next(ids), name, rtype)))
        sent += 1
        if reply["flags"] & 0xF == NXDOMAIN:
            show("  no such name")
            return [], sent
        if reply["answer"]:
            for r in reply["answer"]:
                show(f"  answer: {r[0]} {r[1]} {text(r[3])} (lifetime {r[2]} s)")
            return reply["answer"], sent
        if not reply["authority"]:
            show("  the name exists, but has no such record")
            return [], sent
        ns = reply["authority"][0]
        glue = [g for g in reply["additional"] if g[0] == ns[3]][0]
        show(f"  referral: {ns[0]} is served by {ns[3]} at {glue[3]}")
        server = glue[3]


def text(data):
    return " ".join(map(str, data)) if isinstance(data, tuple) else data


def send(address, data):                         # one round trip on the toy network
    return NETWORK[address].answer(data)


if __name__ == "__main__":
    for name, rtype in (("www.brenmoor.test", "A"), ("library.brenmoor.test", "A"),
                        ("nowhere.brenmoor.test", "A")):
        _, n = resolve(name, rtype, send)
        print(f"  ({n} queries)")
