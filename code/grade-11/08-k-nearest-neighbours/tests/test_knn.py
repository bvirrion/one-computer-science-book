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


def test_data():
    p = load("listings", "parcels")
    items = p.make_items()
    assert len(items) == 300 and items == p.make_items()
    tr, va, te = p.split(items)
    assert (len(tr), len(va), len(te)) == (180, 60, 60)


def test_knn_agrees_with_exercise():
    knn = load("listings", "knn")
    ex = load("exercises", "knn_ex")
    rng = random.Random(8)
    for _ in range(100):
        train = [(rng.random(), rng.random(), rng.choice("ABC")) for _ in range(20)]
        x = (rng.random(), rng.random(), "?")
        for k in (1, 3, 5):
            assert knn.predict(train, x, k) == ex.knn_predict(train, x, k)


def test_results():
    er = load("listings", "error_rate")
    so = load("listings", "sorting_office")
    assert er.error_rate(er.train, er.train, 1, er.scaled) == 0
    assert so.k == 5
    assert er.error_rate(er.train, so.test, 5, er.scaled) < 0.1


def test_exercises():
    ex = load("exercises", "knn_ex")
    assert ex.distance((0, 0, "?"), (3, 4, "?")) == 5
    assert ex.knn_predict(ex.TINY, (4, 4, "?"), 3) == "B"
    order = sorted(ex.TINY, key=lambda e: ex.distance(e, (3.5, 3, "?")))
    assert [e[:2] for e in order] == [(4, 3), (3, 2), (5, 4), (2, 1), (1, 1)]
    items = [(random.Random(i).random(), i % 3, "AB"[i % 2]) for i in range(30)]
    assert ex.loo_error_buggy(items, 1) == 0
    assert ex.loo_error(items, len(items) - 1) >= 0
    s = ex.minmax(ex.TINY)
    assert s((1, 1, "A")) == (0.0, 0.0, "A") and s((5, 4, "B")) == (1.0, 1.0, "B")
    assert ex.weighted_predict(ex.TINY, (4.9, 3.9, "?"), 5) == "B"
