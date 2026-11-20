"""checker.py: a proof checker for natural deduction, one rule at a time."""
from dataclasses import dataclass

from formulas import And, Bot, Forall, Imp, Not, Or, Var, free, parse, show, subst


@dataclass(frozen=True)
class Proof:
    rule: str
    goal: object  # the formula this step concludes
    premises: tuple = ()  # the proofs of its premises
    term: object = None  # forall: the variable introduced, or the term instantiated


def step(rule, goal, *premises, term=None):
    """A proof step written with formulas as text."""
    t = parse(f"T({term})").args[0] if term else None
    return Proof(rule, parse(goal), premises, t)


class ProofError(Exception):
    pass


def check(p, hypotheses, extra=None):
    """Check that p proves hypotheses |- p.goal; return the number of steps checked.
    extra maps more rule names to functions (p, gamma, sub, need) -> steps."""
    gamma = frozenset(parse(h) if isinstance(h, str) else h for h in hypotheses)
    goal = p.goal
    above = [q.goal for q in p.premises]

    def need(condition, why):
        if not condition:
            raise ProofError(f"{p.rule} giving {show(goal)}: {why}")

    def sub(i, *added):  # check premise i, with the hypotheses it may add
        return check(p.premises[i], gamma | set(added), extra)

    if extra and p.rule in extra:
        return extra[p.rule](p, gamma, sub, need)
    need(p.rule in ARITY, "unknown rule")
    need(len(above) == ARITY[p.rule], f"needs {ARITY[p.rule]} premises")
    match p.rule:
        case "hyp":
            need(goal in gamma, "not a hypothesis")
            return 1
        case "and_i":
            need(goal == And(above[0], above[1]), "not the conjunction of the premises")
            return 1 + sub(0) + sub(1)
        case "and_e1" | "and_e2":
            need(isinstance(above[0], And), "the premise is not a conjunction")
            side = above[0].left if p.rule == "and_e1" else above[0].right
            need(goal == side, "not that side of the conjunction")
            return 1 + sub(0)
        case "or_i1" | "or_i2":
            need(isinstance(goal, Or), "not a disjunction")
            side = goal.left if p.rule == "or_i1" else goal.right
            need(above[0] == side, "not that side of the disjunction")
            return 1 + sub(0)
        case "or_e":  # from A | B, and C both from A and from B, conclude C
            need(isinstance(above[0], Or), "the first premise is not a disjunction")
            need(above[1] == goal == above[2], "the cases do not both give the goal")
            return 1 + sub(0) + sub(1, above[0].left) + sub(2, above[0].right)
        case "imp_i":  # from B under the hypothesis A, conclude A -> B
            need(isinstance(goal, Imp) and above[0] == goal.right, "not A -> B from B")
            return 1 + sub(0, goal.left)
        case "imp_e":  # modus ponens
            need(above[0] == Imp(above[1], goal), "the premises are not A -> B and A")
            return 1 + sub(0) + sub(1)
        case "not_i":  # from false under the hypothesis A, conclude ~A
            need(isinstance(goal, Not) and above[0] == Bot(), "not ~A from false")
            return 1 + sub(0, goal.body)
        case "not_e":
            need(goal == Bot() and above[1] == Not(above[0]), "premises not A, ~A")
            return 1 + sub(0) + sub(1)
        case "bot_e":
            need(above[0] == Bot(), "the premise is not false")
            return 1 + sub(0)
        case "raa":  # reductio: from false under ~A, conclude A
            need(above[0] == Bot(), "the premise is not false")
            return 1 + sub(0, Not(goal))
        case "forall_i":  # from A[y/x], y free in no hypothesis, conclude forall x. A
            need(isinstance(goal, Forall) and isinstance(p.term, Var), "no variable")
            y = p.term.name
            need(above[0] == subst(goal.body, goal.var, p.term), f"not A[{y}/x]")
            need(y not in free(goal), f"{y} is free in the conclusion")
            need(all(y not in free(h) for h in gamma), f"{y} is free in a hypothesis")
            return 1 + sub(0)
        case "forall_e":  # from forall x. A, conclude A[t/x]
            need(isinstance(above[0], Forall), "the premise is not universal")
            need(goal == subst(above[0].body, above[0].var, p.term), "not A[t/x]")
            return 1 + sub(0)


ARITY = {"hyp": 0, "and_i": 2, "and_e1": 1, "and_e2": 1, "or_i1": 1, "or_i2": 1,
         "or_e": 3, "imp_i": 1, "imp_e": 2, "not_i": 1, "not_e": 2, "bot_e": 1,
         "raa": 1, "forall_i": 1, "forall_e": 1}
