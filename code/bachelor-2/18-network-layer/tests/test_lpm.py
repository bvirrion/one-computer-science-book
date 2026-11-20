"""The trie and the linear scan agree; at most 32 steps; header, NAT, fragments."""
import random

import fragment
import ipv4_header
import lpm_linear
from cidr import dotted
from lpm_trie import Trie
from nat_sim import NAT


def test_trie_equals_linear():
    rng = random.Random(1)
    prefixes = {"0.0.0.0/0"}
    while len(prefixes) < 300:
        p = rng.randrange(0, 33)
        prefixes.add(f"{dotted(rng.getrandbits(p) << (32 - p) if p else 0)}/{p}")
    table = [(p, k) for k, p in enumerate(sorted(prefixes))]
    t = Trie()
    for p, k in table:
        t.insert(p, k)
    for _ in range(2000):
        a = dotted(rng.getrandbits(32))
        hop, steps = t.lookup(a)
        assert hop == lpm_linear.lookup(table, a) and steps <= 32


def test_header_checksum_and_forward():
    h = ipv4_header.header("198.51.100.3", "203.0.113.10", payload_len=100, ttl=3)
    assert ipv4_header.ones_sum(h) == 0xFFFF
    for ttl in (2, 1, 0):
        h = ipv4_header.forward(h)
        assert h[8] == ttl and ipv4_header.ones_sum(h) == 0xFFFF


def test_nat():
    nat = NAT()
    _, p1, _, _ = nat.outbound("192.168.1.10", 5000, "198.51.100.20", 80)
    _, p2, _, _ = nat.outbound("192.168.1.11", 5000, "198.51.100.20", 80)
    assert p1 != p2 and nat.outbound("192.168.1.10", 5000, "x", 1)[1] == p1
    assert nat.inbound("198.51.100.20", 80, p2)[2:] == ("192.168.1.11", 5000)
    assert nat.inbound("198.51.100.20", 80, 1) is None


def test_fragments_cover_payload():
    for payload in range(1, 5000, 37):
        for mtu in (68, 576, 1500):
            frags = fragment.fragment(payload, mtu)
            assert sum(s for _, s, _ in frags) == payload
            assert all(s % 8 == 0 and more for _, s, more in frags[:-1])
            assert not frags[-1][2]
            assert all(20 + s <= mtu for _, s, _ in frags)
            pos = 0
            for off, s, _ in frags:
                assert off * 8 == pos
                pos += s
