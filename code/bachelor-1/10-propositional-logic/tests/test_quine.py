"""Quine's algorithm against brute force; the colouring and the committee."""

import random
import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "figures"))

import colouring_layout  # noqa: E402
from colouring import COLOURS, colouring_cnf, friendships  # noqa: E402
from committee import RULES, by_permutations, next_to, seating_clauses  # noqa: E402
from quine import quine, satisfies  # noqa: E402
from quine_units import quine_units  # noqa: E402


def brute(clauses, n):
    names = [f"x{i}" for i in range(n)]
    return any(satisfies({x if b else "~" + x for x, b in zip(names, bits)}, clauses)
               for bits in product([False, True], repeat=n))


def test_random_3cnf():
    rng = random.Random(10)
    for _ in range(300):
        n, m = rng.randint(3, 8), rng.randint(1, 40)
        clauses = [frozenset(("~" if rng.random() < 0.5 else "") + f"x{v}"
                             for v in rng.sample(range(n), 3)) for _ in range(m)]
        for solver in (quine, quine_units):
            model = solver(clauses, {"nodes": 0})
            assert (model is not None) == brute(clauses, n)
            if model is not None:
                assert satisfies(model, clauses)


def test_colouring():
    edges = friendships()
    people = sorted({p for e in edges for p in e})
    assert quine(colouring_cnf(people, edges, COLOURS[:2]), {"nodes": 0}) is None
    model = quine(colouring_cnf(people, edges, COLOURS), {"nodes": 0})
    colour = {p: next(c for c in COLOURS if f"{c}{p}" in model) for p in people}
    assert all(colour[a] != colour[b] for a, b in edges)


def test_figure_is_current():
    text = (HERE.parent / "figures" / "colouring_graph.tex").read_text()
    assert text == "\n".join(colouring_layout.lines()) + "\n"


def test_committee():
    good = by_permutations(RULES)
    assert len(good) == 8
    model = quine(seating_clauses(RULES), {"nodes": 0})
    row = "".join(m for _, m in sorted((int(x[1:]), x[0]) for x in model
                                      if len(x) == 2 and x[0] in "ABCDEFG"))
    assert row in good
    harder = RULES | {"Farid next to Elena": next_to("F", "E")}
    assert quine_units(seating_clauses(harder), {"nodes": 0}) is None
    assert by_permutations(harder) == []
