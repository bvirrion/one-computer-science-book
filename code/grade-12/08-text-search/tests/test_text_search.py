import importlib.util
import io
import random
import re
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


def all_positions(text, p):
    return [m.start() for m in re.finditer(f"(?={re.escape(p)})", text)]


def test_searches_agree():
    nv = load("listings", "naive")
    hs = load("listings", "horspool")
    ex = load("exercises", "ts_ex")
    rng = random.Random(6)
    for _ in range(400):
        alphabet = rng.choice(["AB", "ACGT", "abcde "])
        text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
        p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 5)))
        expected = all_positions(text, p)
        found, _ = nv.search_naive(text, p)
        found_h, _ = hs.horspool(text, p)
        assert found == found_h == expected
        assert ex.count_occurrences(text, p) == len(expected)
        assert ex.horspool_first(text, p) == (expected[0] if expected else -1)
        pattern = re.compile("(?=" + "".join("." if ch == "?" else re.escape(ch)
                                              for ch in p.replace("A", "?")) + ")")
        assert ex.search_wildcard(text, p.replace("A", "?")) == [
            m.start() for m in pattern.finditer(text)]


def test_worst_cases_and_tables():
    nv = load("listings", "naive")
    hs = load("listings", "horspool")
    st = load("listings", "shift_table")
    ex = load("exercises", "ts_ex")
    for n, m in [(100, 3), (200, 10), (50, 50)]:
        assert nv.search_naive("a" * n, "a" * (m - 1) + "b")[1] == (n - m + 1) * m
        assert hs.horspool("a" * n, "b" + "a" * (m - 1))[1] == (n - m + 1) * m
    assert st.shift_table("STATION") == {"S": 6, "T": 3, "A": 4, "I": 2, "O": 1}
    assert st.shift_table("BANANA") == {"B": 5, "A": 2, "N": 1}
    assert ex.shift_table_bad("TOWN")["N"] == 0
    assert ex.search_naive_short("the town", "town") == []
    assert ex.search_ignore_case("The Town and the town", "TOWN") == [4, 17]
    table, table_mean, count, mean = ex.mean_jump_measured(200_000, 32, 1)
    assert table == {"C": 3, "G": 1, "T": 5, "A": 4} and table_mean == 3.25
    assert count == 61343 and round(mean, 2) == 3.26


def test_outputs_numbers(monkeypatch):
    monkeypatch.chdir(HERE / "listings")
    load("listings", "town_titles")
    load("listings", "compare_counts")
