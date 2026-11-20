"""quine_units.py: Quine's algorithm with unit propagation, against the plain one."""

from colouring import COLOURS, colouring_cnf, friendships
from committee import RULES, next_to, seating_clauses
from puzzle import clauses as dinner
from quine import assign, neg, quine


def quine_units(clauses, stats):
    stats["nodes"] += 1
    forced = set()
    while frozenset() not in clauses:
        unit = next((c for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        (lit,) = unit  # a clause of one literal: that literal must be true
        forced.add(lit)
        clauses = assign(clauses, lit)
    if frozenset() in clauses:
        return None
    if not clauses:
        return forced
    x = min(clauses[0], key=lambda lit: lit.lstrip("~")).lstrip("~")
    for lit in (x, neg(x)):
        model = quine_units(assign(clauses, lit), stats)
        if model is not None:
            return model | forced | {lit}
    return None


if __name__ == "__main__":
    edges = friendships()
    people = sorted({p for edge in edges for p in edge})
    cases = {"dinner": dinner,
             "2 colours": colouring_cnf(people, edges, COLOURS[:2]),
             "3 colours": colouring_cnf(people, edges, COLOURS),
             "committee": seating_clauses(RULES),
             "committee + 1": seating_clauses(
                 RULES | {"Farid next to Elena": next_to("F", "E")})}
    print(f"{'CNF':14} {'clauses':>7} {'plain':>8} {'units':>6}  satisfiable")
    for name, clauses in cases.items():
        plain, units = {"nodes": 0}, {"nodes": 0}
        a, b = quine(clauses, plain), quine_units(clauses, units)
        assert (a is None) == (b is None)
        print(f"{name:14} {len(clauses):7d} {plain['nodes']:8d} {units['nodes']:6d}"
              f"  {a is not None}")
