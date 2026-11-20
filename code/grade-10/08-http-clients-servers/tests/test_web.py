import importlib.util
import io
import sys
import threading
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from http.server import HTTPServer
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))
sys.path.insert(0, str(HERE / "exercises"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


class Quiet:
    def log_request(self, code="-", size="-"):
        pass


@pytest.fixture
def plus():
    sp = load("exercises", "site_plus")
    handler = type("QuietPlus", (Quiet, sp.PlusHandler), {})
    server = HTTPServer(("127.0.0.1", 42095), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield "http://127.0.0.1:42095", sp
    server.shutdown()
    server.server_close()


def test_query_params():
    q = load("exercises", "query_params").query_params
    assert q("http://h/p?title=forest&genre=nature#top") == {
        "title": "forest", "genre": "nature"}
    assert q("http://h/p") == {} and q("http://h/p?a=") == {"a": ""}


def test_responses_and_request_bytes():
    b = load("exercises", "build_response")
    good = b.response(200, "OK", b"hi")
    assert good.endswith(b"\r\n\r\nhi") and b"Content-Length: 2" in good
    assert b"\r\n\r\n" not in b.response_buggy(200, "OK", b"hi")
    assert b.request_bytes("GET", "/hello", [("Host", "127.0.0.1"),
                                              ("Connection", "close")]) == 59


def test_sum_and_404(plus):
    base, _ = plus
    with urllib.request.urlopen(base + "/sum?a=2&b=40") as r:
        assert r.read() == b"42\n"
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(base + "/sum?a=2")
    assert e.value.code == 400
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(base + "/nowhere")
    assert e.value.code == 404


def test_session_keeps_data_on_server(plus):
    base, sp = plus
    import http.cookiejar
    jar = http.cookiejar.CookieJar()
    browser = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    browser.open(base + "/basket?add=bread").read()
    assert browser.open(base + "/basket?add=milk").read() == b"bread, milk\n"
    (cookie,) = list(jar)
    assert sp.SESSIONS[cookie.value] == ["bread", "milk"]


def test_redirect_loop_is_stopped(plus):
    base, _ = plus
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(base + "/a")
    assert e.value.code == 302


def test_page_cost():
    pc = load("exercises", "page_cost")
    got = pc.fetch_page(42096)
    assert [p for p, _ in got] == ["page.html", "style.css", "logo.svg", "map.svg",
                                   "clock.svg"]
    assert sum(s for _, s in got) == 1129
    assert pc.round_trips(5, False) == 10 and pc.round_trips(5, True) == 6
