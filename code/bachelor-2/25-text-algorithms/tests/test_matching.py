"""Every matcher finds exactly the occurrences that str.startswith finds."""
from hypothesis import given, settings
from hypothesis import strategies as st

from boyer_moore import boyer_moore
from exo_aho import search as aho
from exo_bm_all import boyer_moore_all
from exo_rk_multi import rk_multi
from kmp import failure, kmp
from kmp_automaton import automaton, run
from naive import naive
from rabin_karp import rabin_karp

texts = st.text(alphabet="abc", max_size=60)
patterns = st.text(alphabet="abc", min_size=1, max_size=6)


def occurrences(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]


@settings(max_examples=600, deadline=None)
@given(texts, patterns)
def test_matchers(text, pattern):
    expected = occurrences(text, pattern)
    assert naive(text, pattern)[0] == expected
    assert boyer_moore(text, pattern)[0] == expected
    assert boyer_moore_all(text, pattern)[0] == expected
    found, comparisons = kmp(text, pattern)
    assert found == expected
    assert comparisons <= max(0, 2 * len(text) - len(pattern))
    for q in (7, 1_000_003):  # a tiny modulus makes many spurious hits, never a wrong answer
        assert rabin_karp(text, pattern, q)[0] == expected
    delta = automaton(pattern, "abc")
    assert run(delta, len(pattern), text) == [s + len(pattern) - 1 for s in expected]


@settings(max_examples=300, deadline=None)
@given(texts, st.lists(patterns, min_size=1, max_size=5, unique=True))
def test_multi(text, pats):
    found = sorted(aho(text, pats))
    assert found == sorted((s, p) for p in pats for s in occurrences(text, p))
    same = [p for p in pats if len(p) == len(pats[0])]
    assert rk_multi(text, same) == {p: occurrences(text, p) for p in same}


@settings(max_examples=300, deadline=None)
@given(patterns)
def test_failure_is_longest_border(p):
    pi = failure(p)
    for q in range(1, len(p) + 1):
        borders = [k for k in range(q) if p[:k] == p[q - k:q]]
        assert pi[q] == max(borders)


def test_naive_worst_case():
    n, m = 300, 20
    assert naive("a" * n, "a" * (m - 1) + "b")[1] == m * (n - m + 1)
