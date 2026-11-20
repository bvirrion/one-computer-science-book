"""HTTP: persistent connections, HEAD, chunked bodies; the cache law; the budget."""
import http.client
import math

import http_server
import resolver_cache
from chunked import dechunk

http_server.serve(44207)


def test_keep_alive_and_head():
    http_server.stats.update(connections=0, requests=0)
    conn = http.client.HTTPConnection("127.0.0.1", 44207)
    for method in ("GET", "HEAD", "GET"):
        conn.request(method, "/harbour")
        reply = conn.getresponse()
        body = reply.read()
        assert reply.status == 200
        assert int(reply.getheader("Content-Length")) == len(http_server.PAGES["/harbour"])
        assert body == (b"" if method == "HEAD" else http_server.PAGES["/harbour"])
    conn.request("GET", "/nowhere")
    assert conn.getresponse().status == 404
    assert http_server.stats == {"connections": 1, "requests": 4}


def test_dechunk():
    data = b"4\r\nWiki\r\n6;x=1\r\npedia \r\nE\r\nin \r\n\r\nchunks.\r\n0\r\n\r\nNEXT"
    body, used = dechunk(data)
    assert body == b"Wikipedia in \r\n\r\nchunks." and data[used:] == b"NEXT"
    for cut in (data[:10], data[:-6], b"5\r\nWiki\r\n0\r\n\r\n"):
        try:
            dechunk(cut)
            raise AssertionError("accepted a broken body")
        except ValueError:
            pass


def test_cache_law():
    for rate, life in ((1 / 60, 60), (1 / 600, 3600)):
        rt = rate * life
        assert math.isclose(resolver_cache.hit_fraction(rate, life, n=50_000),
                            rt / (1 + rt), abs_tol=0.01)
