"""Exercises 9 and 10: tests for a compound condition, and rebuilds after an edit."""

from itertools import product


def all_combinations(k):
    return list(product([False, True], repeat=k))


def unique_cause_tests(k):
    """For c1 and c2 and ... and ck: all true, then each one false alone."""
    tests = [tuple([True] * k)]
    for i in range(k):
        t = [True] * k
        t[i] = False
        tests.append(tuple(t))
    return tests


def test_combinations_and_unique_cause():
    for k in range(1, 8):
        assert len(all_combinations(k)) == 2**k
        tests = unique_cause_tests(k)
        assert len(tests) == k + 1
        # each condition, flipped alone between two tests of the set, flips the outcome
        for i in range(k):
            pair = [t for t in tests if all(t[j] for j in range(k) if j != i)]
            assert {all(t) for t in pair} == {True, False}


GRAPH = {  # target: prerequisites, as in the problem's library.Makefile
    "checker": ["loans_main.o", "loans.o", "csv.o", "date.o"],
    "loans_main.o": ["loans_main.c", "loans.h", "date.h"],
    "loans.o": ["loans.c", "loans.h", "date.h", "csv.h"],
    "csv.o": ["csv.c", "csv.h"],
    "date.o": ["date.c", "date.h"],
}


def rebuilt(edited):
    out, changed = set(), True
    while changed:
        changed = False
        for target, prereqs in GRAPH.items():
            if target not in out and any(p == edited or p in out for p in prereqs):
                out.add(target)
                changed = True
    return out


def test_rebuild_counts():
    sources = ["date.h", "date.c", "csv.h", "csv.c", "loans.h", "loans.c", "loans_main.c"]
    compiles = {s: len([t for t in rebuilt(s) if t.endswith(".o")]) for s in sources}
    assert compiles == {"date.h": 3, "date.c": 1, "csv.h": 2, "csv.c": 1, "loans.h": 2, "loans.c": 1,
                        "loans_main.c": 1}
    assert sum(compiles.values()) == 11 and 4 * len(sources) == 28
    assert all("checker" in rebuilt(s) for s in sources)
