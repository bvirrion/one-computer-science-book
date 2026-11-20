import importlib.util
import io
import random
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


def test_bst_against_sorted_set():
    bst = load("listings", "bst")
    node = load("listings", "node")
    tr = load("listings", "traversals")
    ex = load("exercises", "trees_ex")
    rng = random.Random(8)
    for _ in range(200):
        keys = [rng.randint(0, 60) for _ in range(rng.randint(0, 40))]
        t = bst.build(keys)
        assert tr.inorder(t) == sorted(set(keys))
        assert node.size(t) == len(set(keys))
        assert ex.is_bst(t)
        h = node.height(t)
        assert h + 1 <= node.size(t) <= 2 ** (h + 1) - 1 or t is None
        for k in range(61):
            assert (bst.search(t, k) is not None) == (k in keys)
        if keys:
            assert ex.bst_min(t) == min(keys)
            assert tr.inorder(ex.rebuild(tr.preorder(t), tr.inorder(t))) == tr.inorder(t)
            assert tr.preorder(ex.rebuild(tr.preorder(t), tr.inorder(t))) == tr.preorder(t)
        t2 = None
        for k in keys:
            t2 = ex.insert_fixed(t2, k)
        assert tr.preorder(t2) == tr.preorder(t)


def test_listings():
    tr = load("listings", "traversals")
    t = tr.Node("A", tr.Node("B", tr.Node("D"), tr.Node("E", tr.Node("G"))),
                tr.Node("C", None, tr.Node("F")))
    assert "".join(tr.breadth_first(t)) == "ABCDEFG"
    e = load("listings", "expression_tree")
    assert e.evaluate(e.e) == 21
    rh = load("listings", "random_heights")
    h = rh.heights()
    assert (min(h), max(h), round(sum(h) / len(h), 2)) == (16, 31, 21.13)


def test_exercises():
    ex = load("exercises", "trees_ex")
    tr = load("listings", "traversals")
    N = ex.Node
    assert not ex.is_bst(N(5, N(3, None, N(6)), N(8))) and ex.is_bst_wrong(N(5, N(3, None, N(6)), N(8)))
    t = None
    for k in [50, 30, 70]:
        t = ex.insert_broken(t, k)
    assert tr.preorder(t) == [50]
    assert [ex.count_shapes(n) for n in range(6)] == [1, 1, 2, 5, 14, 42]
    t = load("listings", "bst").build([50, 30, 70, 20, 40, 60, 80, 35])
    assert [ex.count_at_depth(t, d) for d in range(5)] == [1, 2, 4, 1, 0]
    assert tr.breadth_first(t) == [50, 30, 70, 20, 40, 60, 80, 35]
