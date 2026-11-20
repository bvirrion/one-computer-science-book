import html
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import acl  # noqa: E402
import ex5_path  # noqa: E402
import ex6_csrf  # noqa: E402
import ex11_roles  # noqa: E402
import login_sql  # noqa: E402
import webapp  # noqa: E402


def run_c(src, flags, stdin, tmp_path):
    exe = tmp_path / "prog"
    subprocess.run(
        ["gcc", "-std=c17", *flags, "-o", exe, src], check=True, cwd=HERE / "listings"
    )
    r = subprocess.run(
        ["setarch", "-R", exe], input=stdin, capture_output=True, text=True
    )
    return r.returncode, r.stdout + r.stderr


@pytest.mark.skipif(not shutil.which("gcc"), reason="needs gcc")
def test_overflow_offsets_and_defences(tmp_path):
    src = HERE / "listings" / "toy_login.c"
    plain = ["-O0", "-fno-stack-protector"]
    _, out = run_c(src, plain, "a" * 28 + "\n" + "a" * 28 + "X\n", tmp_path)
    assert out.count("admin desk opened") == 1  # 29 bytes and not 28 (problem)
    canary = ["-O0", "-fstack-protector-all"]
    code, out = run_c(src, canary, "a" * 24 + "\n", tmp_path)
    assert code == 0 and "reader desk" in out  # exercise 7: 24 bytes pass
    code, out = run_c(src, canary, "a" * 25 + "\n", tmp_path)
    assert code != 0 and "stack smashing detected" in out  # 25 abort
    fixed = HERE / "listings" / "toy_login_fixed.c"
    _, out = run_c(fixed, plain, "a" * 15 + "\n" + "a" * 28 + "X\n", tmp_path)
    assert out.count("hello") == 1 and "admin" not in out
    code, out = run_c(HERE / "exercises" / "ex9_checked_alloc.c", ["-O2"], "", tmp_path)
    assert out.splitlines()[-1] == "count 536870913: refused"
    assert (2**29 + 1) * 8 % 2**32 == 8


def test_sql_injection_and_parameters():
    assert login_sql.login_unsafe("admin' --", "x") == ("admin", "admin")
    assert login_sql.login_safe("admin' --", "x") is None
    assert login_sql.login_safe("ada", "correct horse") == ("ada", "reader")


@settings(max_examples=200, deadline=None)
@given(st.text())
def test_parameters_never_change_the_query(name):
    # any typed name is compared as a value: it logs in only if it is a real name
    assert login_sql.login_safe(name, "correct horse") in (None, ("ada", "reader"))


@settings(max_examples=200, deadline=None)
@given(st.text())
def test_escaped_text_contains_no_markup(text):
    out = html.escape(text)
    assert "<" not in out and ">" not in out and '"' not in out
    assert html.unescape(out) == text  # exercise 10: rendered as the same text


def test_app_escapes_and_checks_tokens():
    for safe in (False, True):
        app = webapp.App(safe)
        cookie = ex6_csrf.new_session(app.sessions, "eve")
        csrf = app.sessions[cookie]["csrf"]
        assert app.comment(cookie, {"text": "<b>hi</b>", "csrf": csrf})[0] == 200
        page = app.page(cookie)[1]
        assert ("<b>hi</b>" in page) != safe
        status, _ = app.renew(cookie, {"weeks": "52"})  # no token
        assert status == (403 if safe else 200)
        assert app.renew(cookie, {"weeks": "2", "csrf": csrf})[0] == 200
        assert app.renew(cookie, {"weeks": "2", "csrf": csrf[:-1] + "?"})[0] == (
            403 if safe else 200
        )


def test_path_traversal(tmp_path):
    public = tmp_path / "public"
    public.mkdir()
    (public / "hours.txt").write_text("open 9-17")
    (tmp_path / "secret.txt").write_text("staff codes")
    assert ex5_path.serve_buggy(public, "../secret.txt") == "staff codes"
    assert ex5_path.serve_fixed(public, "hours.txt") == "open 9-17"
    for bad in ("../secret.txt", "../public/../secret.txt", "/etc/hostname", ".", ""):
        with pytest.raises(PermissionError):
            ex5_path.serve_fixed(public, bad)
    (public / "link.txt").symlink_to(tmp_path / "secret.txt")
    with pytest.raises(PermissionError):
        ex5_path.serve_fixed(public, "link.txt")


def test_roles_and_acl():
    m = ex11_roles.matrix()
    assert m["visitor"] == [True] + [False] * 6
    for rights in ex11_roles.ROLES.values():
        for route in rights:
            assert route in ex11_roles.ROUTES
    assert not ex11_roles.allowed("admin", "renew_any_loan")
    assert not ex11_roles.allowed("nobody", "view_page")
    assert acl.export_confused("eve", "fines.csv").startswith("report")
    assert acl.export_fixed("eve", "fines.csv") == "refused"
    assert acl.export_fixed("ada", "ada-notes.txt").startswith("report")


def test_exercise_numbers():
    s = "Tom & Jerry's <b>\"best\"</b>"
    assert html.escape(s) == "Tom &amp; Jerry&#x27;s &lt;b&gt;&quot;best&quot;&lt;/b&gt;"
    assert (2**32 - 1) // 8 == 536_870_911 and (2**29 * 8) % 2**32 == 0
    assert int.from_bytes(b"X\0\0\0", "little") == 88
    assert (67 - 58, 69 - 58, 136 - 58, 21896 - 16280) == (9, 11, 78, 5616)
