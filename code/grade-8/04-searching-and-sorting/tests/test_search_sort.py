"""Grade 8, chapter 4: searching and sorting."""

import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

from binary_search import binary_search  # noqa: E402
from count_comparisons import mixed  # noqa: E402
from insertion_sort import insertion_sort  # noqa: E402
from linear_search import linear_search  # noqa: E402
from selection_sort import selection_sort  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def output(name):
    return (HERE / "outputs" / f"{name}.txt").read_text().splitlines()[1:]


def test_searches():
    for target in range(1, 101):
        assert binary_search(list(range(1, 101)), target)[1] <= 7
    assert linear_search([3, 1], 1) == (1, 2)
    assert binary_search(list(range(5)), 9)[0] == -1


def test_sorts_and_counts():
    for n in [10, 100, 1000]:
        for items in [list(range(n)), list(range(n, 0, -1)), mixed(n)]:
            a, b = list(items), list(items)
            assert selection_sort(a) == n * (n - 1) // 2
            c = insertion_sort(b)
            assert a == b == sorted(items)
            assert n - 1 <= c <= n * (n - 1) // 2
        assert insertion_sort(list(range(n))) == n - 1
        assert insertion_sort(list(range(n, 0, -1))) == n * (n - 1) // 2
        assert sorted(mixed(n)) == list(range(n))
    assert output("count_comparisons")[-1].split()[-1] == "252747"


def test_worst_and_million():
    worst = output("worst_guesses")
    assert worst[-1].split()[2] == "20" and 2**20 >= 1_000_000 > 2**19
    for line in worst:
        n, k = int(line.split()[0]), int(line.split()[2])
        assert 2 ** (k - 1) <= n < 2**k
        assert max(binary_search(list(range(n)), t)[1] for t in [0, n - 1]) <= k


def test_exercises():
    assert load("all_positions").all_positions([1, 2, 1], 1) == [0, 2]
    try:
        subprocess.run([sys.executable, "binary_bug.py"], cwd=HERE / "exercises",
                       capture_output=True, timeout=2)
        raise AssertionError("the buggy search should never end")
    except subprocess.TimeoutExpired:
        pass
    r = subprocess.run([sys.executable, "insertion_bug.py"], cwd=HERE / "exercises",
                       capture_output=True, text=True)
    assert r.stdout == "[5, 1, 3]\n"
    r = subprocess.run([sys.executable, "max_guesses.py"], cwd=HERE / "exercises",
                       capture_output=True, text=True)
    assert r.stdout == "at most 10 guesses for 1 to 1000\n"
    books = [{"year": "2001", "title": "B"}, {"year": "1999", "title": "Z"},
             {"year": "2001", "title": "A"}]
    load("sort_books").sort_books(books)
    assert [b["title"] for b in books] == ["Z", "A", "B"]
    words = ["banana", "fig", "kiwi"]
    load("by_length").sort_by_length(words)
    assert words == ["fig", "kiwi", "banana"]
