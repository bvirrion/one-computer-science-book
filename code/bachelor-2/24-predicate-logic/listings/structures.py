"""structures.py: finite structures, satisfaction, and the town as a structure."""
import csv
import itertools
from pathlib import Path

from formulas import And, Bot, Exists, Forall, Fun, Imp, Not, Or, Pred, Var

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


class Structure:
    def __init__(self, domain, relations, functions=None):
        self.domain = list(domain)
        self.relations = relations  # a name -> a set of tuples of elements
        self.functions = functions or {}  # a name -> a Python function on elements
        self.atoms = 0  # atomic formulas evaluated so far

    def value(self, t, env):
        match t:
            case Var(x):
                return env[x]
            case Fun(c, ()) if c not in self.functions:
                return c  # a constant names itself
            case Fun(f, args):
                return self.functions[f](*(self.value(a, env) for a in args))

    def holds(self, f, env=None):
        """A, env |= f, by induction on f; the connectives stop as soon as they know."""
        env = env or {}
        match f:
            case Pred(p, args):
                self.atoms += 1
                vals = tuple(self.value(a, env) for a in args)
                return vals[0] == vals[1] if p == "=" else vals in self.relations[p]
            case Bot():
                return False
            case Not(a):
                return not self.holds(a, env)
            case And(a, b):
                return self.holds(a, env) and self.holds(b, env)
            case Or(a, b):
                return self.holds(a, env) or self.holds(b, env)
            case Imp(a, b):
                return not self.holds(a, env) or self.holds(b, env)
            case Forall(x, a):
                return all(self.holds(a, {**env, x: d}) for d in self.domain)
            case Exists(x, a):
                return any(self.holds(a, {**env, x: d}) for d in self.domain)

    def counterexamples(self, sentence):
        """For forall x1 ... xk. body: the values of x1 ... xk that make body false."""
        names, body = [], sentence
        while isinstance(body, Forall):
            names.append(body.var)
            body = body.body
        return [vals for vals in itertools.product(self.domain, repeat=len(names))
                if not self.holds(body, dict(zip(names, vals)))]


def town():
    """People p1 ... and books b1 ... from the town's tables, with their relations."""
    def rows(name):
        with open(TOWN / f"{name}.csv", newline="") as f:
            return list(csv.DictReader(f))

    person = {m["member_id"]: "p" + m["person_id"] for m in rows("members")}
    loans = [(person[r["member_id"]], "b" + r["book_id"], r["return_date"])
             for r in rows("loans")]
    friends = {("p" + r["person_a"], "p" + r["person_b"]) for r in rows("friendships")}
    relations = {
        "Person": {("p" + r["person_id"],) for r in rows("people")},
        "Book": {("b" + r["book_id"],) for r in rows("books")},
        "Member": {(p,) for p in person.values()},
        "Borrowed": {(p, b) for p, b, _ in loans},
        "Out": {(p, b) for p, b, returned in loans if not returned},  # not yet back
        "Friend": friends | {(b, a) for a, b in friends},  # both ways
    }
    domain = sorted(x for (x,) in relations["Person"] | relations["Book"])
    return Structure(domain, relations)
