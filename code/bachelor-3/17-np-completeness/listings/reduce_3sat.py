"""reduce_3sat.py -- SAT to 3-SAT: every clause becomes clauses of exactly three
literals, with new variables, so that the formula stays satisfiable or unsatisfiable."""
from cnf import brute_force, variables


def to_3sat(clauses):
    fresh = max(variables(clauses), default=0)
    out = []
    for c in clauses:
        if len(c) == 1:  # (a): all four ways to fill two new variables
            y, z = fresh + 1, fresh + 2
            fresh += 2
            out += [[c[0], s * y, t * z] for s in (1, -1) for t in (1, -1)]
        elif len(c) == 2:  # (a or b): one new variable, both signs
            fresh += 1
            out += [[c[0], c[1], fresh], [c[0], c[1], -fresh]]
        elif len(c) == 3:
            out.append(list(c))
        else:  # a chain: (l1 or l2 or y1)(not y1 or l3 or y2)...(not y or l_k-1 or l_k)
            fresh += 1
            out.append([c[0], c[1], fresh])
            for lit in c[2:-2]:
                out.append([-fresh, lit, fresh + 1])
                fresh += 1
            out.append([-fresh, c[-2], c[-1]])
    return out


if __name__ == "__main__":
    formula = [[1], [-1, 2], [1, -2, 3, -4, 5], [-3, -5]]
    print("SAT:  ", formula)
    three = to_3sat(formula)
    print("3-SAT:", three)
    print(f"{len(formula)} clauses on {len(variables(formula))} variables -> "
          f"{len(three)} clauses on {len(variables(three))} variables")
    print("satisfiable:", brute_force(formula) is not None,
          brute_force(three) is not None)
