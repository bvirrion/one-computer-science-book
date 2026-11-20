"""Minimal AVL trees against Fibonacci numbers; search-tree shapes against Catalan numbers."""

import sys
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

from catalan import shapes_by_program, shapes_by_recurrence  # noqa: E402
from minimal_avl import fib, height, is_avl, max_height, minimal, size  # noqa: E402


def test_minimal_avl():
    for h in range(16):
        t = minimal(h)
        assert height(t) == h and is_avl(t) and size(t) == fib(h + 3) - 1
    assert max_height(80) == 7 and max_height(87) == 7 and max_height(88) == 8


def test_catalan():
    assert [shapes_by_program(n) for n in range(6)] == [1, 1, 2, 5, 14, 42]
    assert [shapes_by_recurrence(n) for n in range(8)] == [1, 1, 2, 5, 14, 42, 132, 429]
