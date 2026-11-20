"""dpll.py -- a plain DPLL solver: unit propagation, then branch on a variable and
backtrack. Returns a satisfying assignment (dict) or None. Chapter 18 develops it;
stats counts the decisions (branchings) and conflicts (empty clauses met)."""

stats = {"decisions": 0, "conflicts": 0}


def simplify(clauses, lit):
    """Make lit true: drop the clauses it satisfies, remove -lit from the others."""
    return [[x for x in c if x != -lit] for c in clauses if lit not in c]


def dpll(clauses, assignment=None):
    assignment = dict(assignment or {})
    while True:  # unit propagation
        if any(len(c) == 0 for c in clauses):
            stats["conflicts"] += 1
            return None
        units = [c[0] for c in clauses if len(c) == 1]
        if not units:
            break
        lit = units[0]
        assignment[abs(lit)] = lit > 0
        clauses = simplify(clauses, lit)
    if not clauses:
        return assignment
    var = abs(clauses[0][0])  # branch on the first variable of the first clause
    stats["decisions"] += 1
    for lit in (var, -var):
        result = dpll(simplify(clauses, lit), {**assignment, var: lit > 0})
        if result is not None:
            return result
    return None
