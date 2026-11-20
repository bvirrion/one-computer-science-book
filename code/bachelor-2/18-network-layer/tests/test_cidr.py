"""Prefix arithmetic against ipaddress, on random addresses (hypothesis)."""
import ipaddress

from hypothesis import given
from hypothesis import strategies as st

import cidr
from aggregate import aggregate
from contains import contains
from ipv6_compress import compress
from ipv6_text import expand

addrs = st.integers(0, 2**32 - 1)
lengths = st.integers(0, 32)


@given(addrs, lengths)
def test_network_and_broadcast(a, p):
    net = ipaddress.ip_network((a, p), strict=False)
    assert cidr.network(a, p) == int(net.network_address)
    assert cidr.broadcast(a, p) == int(net.broadcast_address)
    assert cidr.parse(f"{cidr.dotted(a)}/{p}") == (a, p)


@given(addrs, lengths, addrs)
def test_contains(a, p, b):
    net = ipaddress.ip_network((a, p), strict=False)
    prefix = f"{cidr.dotted(a)}/{p}"
    assert contains(prefix, cidr.dotted(b)) == (ipaddress.ip_address(b) in net)


@given(st.lists(st.tuples(st.integers(0, 255), st.integers(22, 26)), max_size=12))
def test_aggregate_minimal(items):
    prefixes = [f"198.51.{n}.0/{p}" for n, p in items]
    nets = [ipaddress.ip_network(p, strict=False) for p in prefixes]
    ref = sorted(str(n) for n in ipaddress.collapse_addresses(nets))
    assert sorted(aggregate(prefixes)) == ref


@given(st.lists(st.sampled_from([0, 0, 0, 1, 0xDB8, 0xFFFF]), min_size=8, max_size=8))
def test_ipv6_text(groups):
    value = int.from_bytes(b"".join(g.to_bytes(2, "big") for g in groups), "big")
    addr = ipaddress.IPv6Address(value)
    assert compress(groups) == str(addr)
    assert expand(str(addr)) == groups
