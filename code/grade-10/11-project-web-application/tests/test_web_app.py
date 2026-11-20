import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def request(path, method="GET", query=None, form=None, cookies=None):
    return {"method": method, "path": path, "query": query or {},
            "form": form or {}, "cookies": cookies or {}}


def test_milestone_routes():
    m1 = load("listings", "app_m1")
    assert m1.dispatch(request("/"))[0] == 200
    assert [m1.dispatch(request(p))[0] for p in ["/book/7", "/book/0", "/book", "/x/y"]] \
        == [200, 404, 404, 404]
    m2 = load("listings", "app_m2")
    text = m2.dispatch(request("/<b>"))[2]
    assert "&lt;b&gt;" in text and "<b>" not in text
    assert m2.dispatch(request("/"))[2].count("<li>") == 80


def test_reserve_and_cookie():
    m3 = load("listings", "app_m3")
    m3.RESERVATIONS.clear()
    status, _, _, headers = m3.dispatch(request("/reserve", "POST",
                                                form={"book": "7", "member": "12"}))
    assert status == 303 and headers == [("Location", "/book/7")]
    assert "Reserved by: 12" in m3.dispatch(request("/book/7"))[2]
    m5 = load("listings", "app_m5")
    headers = m5.dispatch(request("/search", query={"q": "a b"}))[3]
    assert headers[0][1].startswith("last=a%20b;")
    assert "Your last search" in m5.dispatch(request("/", cookies={"last": "a%20b"}))[2]
    assert '"year": 1950' in m5.dispatch(request("/api/book/7"))[2]


def test_exercises():
    ex = load("exercises", "app_ex")
    assert ex.dispatch(request("/about"))[0] == 200
    assert ex.dispatch(request("/author/Zoe Stoneton"))[2].count("<li>") == 7
    pages = [ex.dispatch(request("/", query={"page": str(p)})) for p in range(6)]
    assert [s for s, *_ in pages] == [404, 200, 200, 200, 200, 404]
    assert sum(text.count("<li>") for _, _, text, _ in pages) == 80
    assert ex.dispatch(request("/", query={"sort": "year"}))[0] == 200
    assert ex.dispatch(request("/", query={"sort": "colour"}))[0] == 400
    assert ex.dispatch(request("/reserve"))[3] == [("Allow", "POST")]
    assert ex.reserve_buggy(request("/reserve", "POST",
                                    form={"book": "1", "member": "5"}))[0] == 400
    ex.app_m3.RESERVATIONS.clear()
    codes = [ex.dispatch(request("/reserve", "POST", form={"book": str(b), "member": "5"}))[0]
             for b in (1, 2, 3, 4)]
    assert codes == [303, 303, 303, 409]


def test_unittest_suite_against_real_server():
    run = subprocess.run([sys.executable, "-m", "unittest", "app_tests"],
                         cwd=HERE / "listings", capture_output=True, text=True, timeout=60)
    assert run.returncode == 0, run.stderr
