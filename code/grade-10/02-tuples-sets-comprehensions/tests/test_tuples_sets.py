import importlib.util
import io
import itertools
import random
import sys
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "exercises"))

import town  # noqa: E402


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(module)
        except TypeError:
            pass  # staged errors at the end of a listing
    return module


def test_min_max_matches_builtins():
    min_max = load("listings", "min_max").min_max
    rng = random.Random(2026)
    for _ in range(200):
        t = [rng.randint(-50, 50) for _ in range(rng.randint(1, 12))]
        assert min_max(t) == (min(t), max(t))


def test_shared_books_listing_agrees_with_common_books():
    common = load("exercises", "common_books").common_books
    loans = town.load("loans")
    assert common(loans, 40, 55) == {16, 57, 62, 71, 75}
    assert common(loans, 40, 40) == load("listings", "shared_books").books_of(40)


def test_grid_bug_shares_rows():
    bad, good = load("exercises", "grid_bug").demo()
    assert bad == [[1, 0, 0]] * 3
    assert good == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


def test_subsets_counts_and_distinct():
    subsets = load("exercises", "subsets").subsets
    s = subsets(["a", "b", "c", "d"])
    assert len(s) == 16
    assert len({frozenset(x) for x in s}) == 16
    assert sum(1 for x in s if len(x) == 2) == 6


def test_distinct_authors():
    mod = load("exercises", "distinct_authors")
    books = town.load("books")
    assert len(mod.distinct_authors(books)) == 23
    assert mod.distinct_authors(books) == set(b["author"] for b in books)
    genre = books[0]["genre"]
    assert mod.authors_in_genre(books, genre) == sorted({b["author"] for b in books if b["genre"] == genre})


def test_list_intersection_counts():
    f = load("exercises", "count_intersection").list_intersection
    a = list(range(10))
    b = list(range(100, 110))
    assert f(a, b) == ([], 100)
    assert f([1, 2], [2, 1]) == ([1, 2], 3)


def test_transpose():
    transpose = load("exercises", "transpose").transpose
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    t = [[1, 2], [3, 4], [5, 6]]
    assert transpose(transpose(t)) == t


def test_grid_copy():
    mod = load("exercises", "grid_copy")
    g = [[0, 1], [1, 0]]
    assert mod.next_step(g) == [[1, 0], [0, 1]] and g == [[0, 1], [1, 0]]
    g2 = [[0, 1], [1, 0]]
    mod.next_step_buggy(g2)
    assert g2 == [[1, 0], [0, 1]]  # the caller's grid was changed


def test_jaccard():
    jaccard = load("exercises", "jaccard").jaccard
    assert jaccard({1, 2, 3}, {2, 3, 4}) == Fraction(1, 2)
    with pytest.raises(AssertionError):
        jaccard(set(), set())


def test_readers_alike_result():
    mod = load("exercises", "readers_alike")
    ids, pairs = mod.best_pairs(5)
    assert len(ids) == 49 and len(pairs) == 49 * 48 // 2
    assert pairs[0] == (Fraction(5, 12), 40, 55)
    assert pairs[1][0] < pairs[0][0]
    ids1, pairs1 = mod.best_pairs(1)
    assert pairs1[0] == (Fraction(1, 2), 32, 47)
    # brute force over all pairs with itertools agrees
    best = max(mod.jaccard(mod.books[i], mod.books[j]) for i, j in itertools.combinations(ids, 2))
    assert best == Fraction(5, 12)


def test_tuple_key_staged_error():
    with pytest.raises(TypeError):
        exec((HERE / "listings" / "tuple_key.py").read_text(), {"print": lambda *a: None})
