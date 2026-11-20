"""Binary trees, structural bounds, the conversion of trees of any arity."""

import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from count_paths import count_paths  # noqa: E402
from inductive import Node, height, leaves, shapes, size  # noqa: E402
from lcrs import Tree, from_binary, to_binary  # noqa: E402

trees = st.recursive(st.none(), lambda sub: st.builds(Node, sub, st.integers(0, 9), sub),
                     max_leaves=40)
full = st.recursive(st.builds(Node, st.none(), st.integers(0, 9), st.none()),
                    lambda sub: st.builds(Node, sub, st.integers(0, 9), sub), max_leaves=40)
general = st.recursive(st.builds(Tree, st.integers(0, 9)),
                       lambda sub: st.builds(Tree, st.integers(0, 9), st.lists(sub, max_size=4)),
                       max_leaves=30)


def internal(t):
    return 0 if t is None else size(t) - leaves(t)


def flatten(t):
    return [] if t is None else flatten(t.left) + [t.key] + flatten(t.right)


@given(trees)
def test_bounds(t):
    h = height(t)
    assert h + 1 <= size(t) <= 2 ** (h + 1) - 1
    assert leaves(t) <= 2 ** max(h, 0)
    assert len(flatten(t)) == size(t)
    assert count_paths(t) == leaves(t)


@given(full)
def test_full_trees(t):
    assert leaves(t) == internal(t) + 1 == count_paths(t)


@given(general)
def test_lcrs_round_trip(t):
    b = to_binary(t)
    assert from_binary(b) == [t]
    assert size(b) == count(t)


def count(t):
    return 1 + sum(count(c) for c in t.children)


def test_shape_counts():
    assert [len(shapes(h)) for h in range(-1, 3)] == [1, 2, 5, 26]
    assert all(height(t) <= 2 for t in shapes(2))
