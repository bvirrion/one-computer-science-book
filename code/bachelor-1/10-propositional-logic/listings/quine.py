"""quine.py: Quine's algorithm on a CNF: choose a variable, try both values,
simplify, recurse. A clause is a frozenset of literals such as "p" or "~p"."""


def neg(lit):
    return lit[1:] if lit.startswith("~") else "~" + lit


def assign(clauses, lit):
    """Make lit true: the clauses holding lit are satisfied and vanish,
    and ~lit, now false, leaves the others."""
    return [c - {neg(lit)} for c in clauses if lit not in c]


def quine(clauses, stats):
    """A set of literals whose truth satisfies every clause, or None if no
    valuation does. stats["nodes"] counts the calls (the search-tree nodes)."""
    stats["nodes"] += 1
    if not clauses:
        return set()  # nothing left to satisfy
    if frozenset() in clauses:
        return None  # an empty clause: every literal of it was made false
    x = min(clauses[0], key=lambda lit: lit.lstrip("~")).lstrip("~")
    for lit in (x, neg(x)):
        model = quine(assign(clauses, lit), stats)
        if model is not None:
            return model | {lit}
    return None


def satisfies(model, clauses):
    return all(c & model for c in clauses)


def cnf_of(text):
    """'p ~q, q r' -> [{p, ~q}, {q, r}]: clauses separated by commas."""
    return [frozenset(c.split()) for c in text.split(",")]


if __name__ == "__main__":
    for text in ["p q, ~p q, p ~q, ~p ~q", "p q r, ~p, ~q, r ~s, s ~r"]:
        clauses, stats = cnf_of(text), {"nodes": 0}
        model = quine(clauses, stats)
        print(f"{text:30} model {sorted(model) if model is not None else None}"
              f"  nodes {stats['nodes']}")
