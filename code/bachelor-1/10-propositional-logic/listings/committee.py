"""committee.py: seating seven members in a row of seven seats, by SAT."""

from functools import reduce
from itertools import permutations

from evaluate import value
from exactly import exactly_one
from formula import Var, size
from normal_forms import cnf
from quine import quine, satisfies
from tseitin import tseitin

MEMBERS = "ABCDEFG"  # Alma, Boris, Chloe, Dmitri, Elena, Farid, Greta
SEATS = range(1, 8)


def at(m, s):  # the variable "member m sits in seat s"
    return Var(f"{m}{s}")


def any_of(fs):
    return reduce(lambda a, b: a | b, fs)


def next_to(x, y):
    return any_of([at(x, s) & any_of([at(y, t) for t in (s - 1, s + 1) if t in SEATS])
                   for s in SEATS])


RULES = {"Alma next to Boris": next_to("A", "B"),
         "Chloe not next to Dmitri": ~next_to("C", "D"),
         "Elena at an end": at("E", 1) | at("E", 7),
         "Greta in the middle": at("G", 4),
         "Farid next to Greta": next_to("F", "G"),
         "Chloe next to Elena": next_to("C", "E")}


def seating_clauses(rules):
    clauses = []
    for m in MEMBERS:
        clauses += exactly_one([f"{m}{s}" for s in SEATS])
    for s in SEATS:
        clauses += exactly_one([f"{m}{s}" for m in MEMBERS])
    for k, f in enumerate(rules.values()):
        clauses += tseitin(f, prefix=f"r{k + 1}t")
    return clauses


def by_permutations(rules):
    """The check: try all 7! seatings, a valuation for each."""
    good = []
    for perm in permutations(SEATS):
        v = {f"{m}{s}": perm[i] == s for i, m in enumerate(MEMBERS) for s in SEATS}
        if all(value(f, v) for f in rules.values()):
            good.append("".join(sorted(MEMBERS, key=lambda m: perm[MEMBERS.index(m)])))
    return good


if __name__ == "__main__":
    for name, f in RULES.items():
        print(f"{name:25} size {size(f):3d}  naive CNF {len(cnf(f)):4d} clauses"
              f"  Tseitin {len(tseitin(f)):3d} clauses")
    clauses, stats = seating_clauses(RULES), {"nodes": 0}
    print(len(clauses), "clauses in all")
    model = quine(clauses, stats)
    print("satisfiable:", model is not None, "| nodes:", stats["nodes"],
          "| checked:", satisfies(model, clauses))
    row = sorted((s, m) for m in MEMBERS for s in SEATS if f"{m}{s}" in model)
    print("seating:", "".join(m for _, m in row))
    good = by_permutations(RULES)
    print(len(good), "seatings out of 5040 obey the rules:", *good)
    harder = RULES | {"Farid next to Elena": next_to("F", "E")}
    stats = {"nodes": 0}
    model = quine(seating_clauses(harder), stats)
    print("with Farid next to Elena:", model, "| nodes:", stats["nodes"],
          "| by permutations:", len(by_permutations(harder)))
