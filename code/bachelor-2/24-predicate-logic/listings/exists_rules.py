"""exists_rules.py: the two rules of the existential quantifier, for checker.check."""
from formulas import Exists, Var, free, subst


def exists_i(p, gamma, sub, need):  # from A[t/x], conclude exists x. A
    need(isinstance(p.goal, Exists), "not an existential")
    need(len(p.premises) == 1 and p.term is not None, "needs one premise, a term")
    need(p.premises[0].goal == subst(p.goal.body, p.goal.var, p.term), "not A[t/x]")
    return 1 + sub(0)


def exists_e(p, gamma, sub, need):
    """From exists x. A, and C under the hypothesis A[y/x], conclude C, when y is free
    neither in exists x. A, nor in C, nor in another hypothesis."""
    need(len(p.premises) == 2 and isinstance(p.term, Var), "2 premises, a variable")
    some, y = p.premises[0].goal, p.term.name
    need(isinstance(some, Exists), "the first premise is not an existential")
    need(p.premises[1].goal == p.goal, "the second premise does not give the goal")
    need(y not in free(some) | free(p.goal), f"{y} is free in the conclusion")
    need(all(y not in free(h) for h in gamma), f"{y} is free in a hypothesis")
    return 1 + sub(0) + sub(1, subst(some.body, some.var, Var(y)))


EXISTS = {"exists_i": exists_i, "exists_e": exists_e}
