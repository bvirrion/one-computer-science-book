import ast
import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import ex5_vcgen  # noqa: E402
import ex6_for  # noqa: E402
import ex12_sort  # noqa: E402
import hoare_check  # noqa: E402
import lifts  # noqa: E402
import peterson_mc  # noqa: E402
import pytest  # noqa: E402
from bitblast import Blaster, check  # noqa: E402
from cdcl import CDCL  # noqa: E402
from ctl import Kripke  # noqa: E402
from vcgen import vcgen  # noqa: E402
from verify_bsearch import SEARCH  # noqa: E402
from whilelang import parse, run, value  # noqa: E402
from wp import wp  # noqa: E402


def f(text):
    return ast.parse(text, mode="eval").body


FIXED = SEARCH.replace("MID", "lo + (hi - lo) // 2").replace(
    "INV", "lo <= hi and hi <= n"
)
WRONG = SEARCH.replace("MID", "(lo + hi) // 2").replace("INV", "lo <= hi and hi <= n")


def test_fixed_binary_search_runs_and_verifies():
    rng = random.Random(20)
    for n in range(256):
        env = run(parse(FIXED), {"n": n}, choose=lambda: rng.random() < 0.5)
        assert env["lo"] == env["hi"] <= n
    assert all(check(vc)[0] for _, vc in vcgen("True", FIXED, "lo == hi and hi <= n"))


def test_overflow_counterexample_is_real():
    results = dict((name, check(vc)) for name, vc in vcgen("True", WRONG, "lo == hi"))
    valid, cex, _ = results["preserved"]
    assert not valid
    assert cex["lo"] < cex["hi"] <= cex["n"]
    mid = (cex["lo"] + cex["hi"]) % 256 // 2
    assert not (cex["lo"] <= mid < cex["hi"])
    with pytest.raises(AssertionError):
        run(parse(WRONG), {"n": 255}, choose=lambda: True)


@given(st.integers(0, 255))
def test_wp_agrees_with_running(x):
    program = parse("y = x + 1\nx = y + y")
    pre = wp(program, f("x < 100"))
    after = run(program, {"x": x})
    assert value(pre, {"x": x}, None) == (after["x"] < 100)


EXPRS = [
    "x + y < x",
    "implies(x < y, x + (y - x) // 2 < y)",
    "x - y == y - x",
    "not (x // 2 >= y) or x > y",
    "x + 1 == 0",
    "(x == y) or (x != y and x < y)",
]


@settings(max_examples=60)
@given(st.integers(0, 255), st.integers(0, 255), st.sampled_from(EXPRS))
def test_bitblast_agrees_with_the_interpreter(x, y, text):
    b = Blaster()
    out = b.bit(f(text))
    for name, val in (("x", x), ("y", y)):
        bits = b.word(ast.Name(id=name))
        b.clauses += [[v if val >> i & 1 else -v] for i, v in enumerate(bits)]
    b.clauses.append([out])
    model, _ = CDCL(b.clauses, b.n).solve()
    assert (model is not None) == value(f(text), {"x": x, "y": y}, None)


def test_hoare_derivation(capsys):
    body = (
        "conseq",
        "x <= 10 and x < 10",
        "x <= 10",
        ("assign", "x = x + 1", "x <= 10"),
    )
    p, _, q = hoare_check.derive(
        ("conseq", "x <= 10", "x == 10", ("while", "x < 10", "x <= 10", body))
    )
    assert ast.unparse(p) == "x <= 10" and ast.unparse(q) == "x == 10"
    with pytest.raises(AssertionError):
        hoare_check.derive(
            (
                "conseq",
                "x <= 10 and x < 10",
                "x <= 10",
                ("assign", "x = x + 2", "x <= 10"),
            )
        )


kripkes = st.integers(1, 7).flatmap(
    lambda n: st.tuples(
        st.lists(st.sets(st.integers(0, n - 1), min_size=1), min_size=n, max_size=n),
        st.lists(st.sets(st.sampled_from(["p", "q"])), min_size=n, max_size=n),
    )
)


@given(kripkes)
def test_ctl_fixed_points(kp):
    succ, labels = kp
    k = Kripke(
        {s: set(t) for s, t in enumerate(succ)},
        {s: set(lab) | {"true"} for s, lab in enumerate(labels)},
    )
    reach = {}
    for s in k.states:  # EF q by search: some reachable state satisfies q
        seen, todo = {s}, [s]
        while todo:
            for t in k.succ[todo.pop()]:
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        reach[s] = seen
    assert k.sat(("EF", "q")) == {
        s for s in k.states if any("q" in k.labels[t] for t in reach[s])
    }
    assert k.sat(("AG", "p")) == {
        s for s in k.states if all("p" in k.labels[t] for t in reach[s])
    }
    assert k.sat(("AF", "q")) == k.states - k.sat(("EG", ("not", "q")))


def test_peterson_and_variant():
    succ, _ = peterson_mc.explore(peterson_mc.peterson)
    assert len(succ) == 20
    assert not any(s[0] == s[1] == peterson_mc.CRIT for s in succ)
    succ, parent = peterson_mc.explore(peterson_mc.no_turn)
    assert len(succ) == 9
    assert any(s[0] == s[1] == peterson_mc.CRIT for s in succ)


def test_lifts_state_counts():
    for n in range(1, 7):
        assert lifts.check(n, atomic=True) == ((n + 2) * 2 ** (n - 1), None)
    assert [lifts.check(n, atomic=False)[1] for n in range(1, 5)] == [None, 6, 6, 6]


WRONG_LOOP = "x = 0\nwhile x < 10:\n    invariant(x <= 10)\n    x = x + 1"


def test_exercise_5():
    buggy = ex5_vcgen.vcgen_with(ex5_vcgen.buggy_awp, "True", WRONG_LOOP, "x == 11")
    assert all(check(vc)[0] for _, vc in buggy)
    fixed = ex5_vcgen.vcgen_with(ex5_vcgen.fixed_awp, "True", WRONG_LOOP, "x == 11")
    assert not all(check(vc)[0] for _, vc in fixed)
    right = ex5_vcgen.vcgen_with(ex5_vcgen.fixed_awp, "True", WRONG_LOOP, "x == 10")
    assert all(check(vc)[0] for _, vc in right)


def test_exercise_6():
    good = ex6_for.for_vcs(
        "c == 0 and n < 200", "i", "0", "n", "c == i and n < 200", "c = c + 1", "c == n"
    )
    assert all(check(vc)[0] for _, vc in good)
    bad = ex6_for.for_vcs(
        "c == 0 and n < 200", "i", "0", "n", "c == i and n < 200", "c = c + 2", "c == n"
    )
    assert not all(check(vc)[0] for _, vc in bad)


def test_exercise_12():
    valid, _, size = ex12_sort.verify()
    assert valid and size == (1390, 4538)
    valid, cex, _ = ex12_sort.verify(ex12_sort.program().replace("a2 > a3", "a2 < a3"))
    assert not valid
