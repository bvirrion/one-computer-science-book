"""colouring.py: three colours for the town's friendship graph, by SAT."""

import csv
from pathlib import Path

from quine import quine, satisfies

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"
COLOURS = ["red", "green", "blue"]


def friendships():
    with open(TOWN / "friendships.csv", newline="") as f:
        return [(int(r["person_a"]), int(r["person_b"])) for r in csv.DictReader(f)]


def colouring_cnf(people, edges, colours):
    """Variable red5 says: person 5 is red."""
    clauses = [frozenset(f"{c}{p}" for c in colours) for p in people]  # some colour
    for a, b in edges:  # two friends never share a colour
        clauses += [frozenset([f"~{c}{a}", f"~{c}{b}"]) for c in colours]
    return clauses


if __name__ == "__main__":
    edges = friendships()
    people = sorted({p for edge in edges for p in edge})
    for k in (2, 3):
        clauses, stats = colouring_cnf(people, edges, COLOURS[:k]), {"nodes": 0}
        model = quine(clauses, stats)
        print(f"{k} colours: {len(people) * k} variables, {len(clauses)} clauses,",
              "satisfiable" if model is not None else "unsatisfiable",
              f"({stats['nodes']} nodes)")
    print("model checked:", satisfies(model, clauses))
    colour = {p: next(c for c in COLOURS if f"{c}{p}" in model) for p in people}
    for c in COLOURS:
        print(f"{c:5}:", *[p for p in people if colour[p] == c])
    print("friends of equal colour:", sum(colour[a] == colour[b] for a, b in edges))
