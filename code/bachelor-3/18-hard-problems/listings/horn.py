"""horn.py -- Horn clauses: at most one positive literal. Horn-SAT by forward
propagation in linear time, and a small forward-chaining rule engine on generated
family facts."""
import csv
import random
from pathlib import Path

PEOPLE = Path(__file__).resolve().parents[4] / "data" / "town" / "people.csv"


def horn_sat(clauses, n):
    """Start with every variable false; a clause whose negative literals are all true
    forces its positive one. Each clause keeps a counter of negatives not yet true, so
    every literal is looked at a constant number of times."""
    waiting = [sum(1 for x in c if x < 0) for c in clauses]
    uses = {v: [] for v in range(1, n + 1)}
    for i, c in enumerate(clauses):
        for x in c:
            if x < 0:
                uses[-x].append(i)
    true, queue = set(), [i for i, w in enumerate(waiting) if w == 0]
    while queue:
        c = clauses[queue.pop()]
        head = [x for x in c if x > 0]
        if not head:
            return None  # every premise true, and no conclusion: unsatisfiable
        if head[0] in true:
            continue
        true.add(head[0])
        for i in uses[head[0]]:
            waiting[i] -= 1
            if waiting[i] == 0:
                queue.append(i)
    return {v: v in true for v in range(1, n + 1)}


def parent_facts(seed=18):
    """Generated families: each person gets up to two parents among those born 20 to 45
    years earlier (the town lists no families; these are made up, seeded)."""
    people = [(int(r["person_id"]), r["first_name"], int(r["birth_year"]))
              for r in csv.DictReader(open(PEOPLE))]
    rng, facts = random.Random(seed), set()
    for pid, _, year in people:
        older = [q for q, _, y in people if 20 <= year - y <= 45]
        for q in rng.sample(older, min(2, len(older))):
            facts.add(("parent", q, pid))
    return facts, {pid: name for pid, name, _ in people}


RULES = [  # (premises, conclusion); capital letters are variables
    ([("parent", "X", "Y")], ("ancestor", "X", "Y")),
    ([("parent", "X", "Y"), ("ancestor", "Y", "Z")], ("ancestor", "X", "Z")),
    ([("parent", "X", "Y"), ("parent", "Y", "Z")], ("grandparent", "X", "Z")),
]


def match(premises, facts, binding):
    """Every way of binding the variables so that all premises are known facts."""
    if not premises:
        yield binding
        return
    first, *rest = premises
    for fact in facts:
        if fact[0] != first[0]:
            continue
        b = dict(binding)
        if all(b.setdefault(t, f) == f if t.isupper() else t == f
               for t, f in zip(first[1:], fact[1:])):
            yield from match(rest, facts, b)


def forward_chain(facts, rules):
    """Apply every rule to the known facts until no new fact appears."""
    facts, rounds = set(facts), 0
    while True:
        rounds += 1
        new = {(c[0], *(b[t] for t in c[1:]))
               for premises, c in rules for b in match(premises, facts, {})} - facts
        if not new:
            return facts, rounds
        facts |= new


if __name__ == "__main__":
    clauses = [[1], [-1, 2], [-2, -3, 4], [-1, 3], [-4, -5]]
    print("Horn-SAT:", horn_sat(clauses, 5))
    print("with [5] added:", horn_sat(clauses + [[5]], 5))
    facts, names = parent_facts()
    derived, rounds = forward_chain(facts, RULES)
    for kind in ("parent", "grandparent", "ancestor"):
        print(f"{kind:<12} facts: {sum(f[0] == kind for f in derived):>5}")
    print("rounds until nothing new:", rounds)
    first = min(f for f in derived if f[0] == "grandparent")
    print(f"for example: {names[first[1]]} is a grandparent of {names[first[2]]}")
