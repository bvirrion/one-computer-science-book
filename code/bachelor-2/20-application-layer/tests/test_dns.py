"""DNS: round trips of every record type, compression, pointer checks, resolution."""
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

import dns_message as dm
import resolve
import zone
from caching_resolver import CachingResolver

label = st.text("abcdefghijklmnopqrstuvwxyz0123456789-", min_size=1, max_size=63)
name = st.lists(label, min_size=1, max_size=4).map(".".join)
rdata = {"A": st.ip_addresses(v=4).map(str), "AAAA": st.ip_addresses(v=6).map(str),
         "NS": name, "CNAME": name, "TXT": st.text("abc xyz", max_size=50),
         "MX": st.tuples(st.integers(0, 65535), name)}
record = st.sampled_from(sorted(rdata)).flatmap(
    lambda t: st.tuples(name, st.just(t), st.integers(0, 2**31 - 1), rdata[t]))


@settings(max_examples=200, deadline=None)
@given(st.lists(record, max_size=6), st.booleans())
def test_round_trip(records, compress):
    msg = {"id": 7, "flags": dm.QR, "question": [("a.test", "A")], "answer": records,
           "authority": [], "additional": []}
    assert dm.decode(dm.encode(msg, compress)) == msg
    assert len(dm.encode(msg)) <= len(dm.encode(msg, compress=False))


def test_loops_and_forward_pointers_rejected():
    for bad in (bytes(12) + b"\xc0\x0c", bytes(12) + b"\x01a\xc0\x0e\x00",
                bytes(12) + b"\xc0\x0e\x01a\x00"):
        with pytest.raises(ValueError):
            dm.read_name(bad, 12)


def test_resolution_and_cache():
    records, n = resolve.resolve("library.brenmoor.test", "A", resolve.send,
                                 show=lambda s: None)
    assert n == 3 and records[-1][3] == "127.0.0.1"
    now = [0.0]
    r = CachingResolver(resolve.send, lambda: now[0])
    r.resolve("www.brenmoor.test", "A")
    assert r.queries == 3
    r.resolve("www.brenmoor.test", "A")
    assert r.queries == 3                        # answered from the cache
    r.resolve("mail.brenmoor.test", "A")
    assert r.queries == 4                        # the zone's server is known
    now[0] = 4000                                # past the 3600 s of the A record
    r.resolve("www.brenmoor.test", "A")
    assert r.queries == 5
    now[0] = 200_000                             # past every referral
    r.resolve("www.brenmoor.test", "A")
    assert r.queries == 8


def test_server_answers():
    for q, flags_rcode in ((("nowhere.brenmoor.test", "A"), 3), (("www.brenmoor.test", "MX"), 0)):
        reply = dm.decode(zone.BRENMOOR.answer(dm.query(1, *q)))
        assert reply["flags"] & 0xF == flags_rcode and reply["answer"] == []
