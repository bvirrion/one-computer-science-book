"""formulas.py: first-order terms and formulas: parsing, printing, free variables,
substitution that avoids capture."""
import re
from dataclasses import dataclass

VARIABLE = re.compile(r"[u-z][0-9']*$")  # x, y, z, x1, y'...; other names: constants


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Fun:  # f(t1, ..., tn); a constant is a function with no argument
    name: str
    args: tuple = ()


@dataclass(frozen=True)
class Pred:  # P(t1, ..., tn); the name "=" is equality
    name: str
    args: tuple = ()


@dataclass(frozen=True)
class Bot:  # falsity
    pass


@dataclass(frozen=True)
class Not:
    body: object


@dataclass(frozen=True)
class And:
    left: object
    right: object


@dataclass(frozen=True)
class Or:
    left: object
    right: object


@dataclass(frozen=True)
class Imp:
    left: object
    right: object


@dataclass(frozen=True)
class Forall:
    var: str
    body: object


@dataclass(frozen=True)
class Exists:
    var: str
    body: object


def free(e):
    """The free variables of a term or a formula."""
    match e:
        case Var(x):
            return {x}
        case Fun(_, args) | Pred(_, args):
            return set().union(*map(free, args))
        case Bot():
            return set()
        case Not(a):
            return free(a)
        case And(a, b) | Or(a, b) | Imp(a, b):
            return free(a) | free(b)
        case Forall(x, a) | Exists(x, a):
            return free(a) - {x}  # x is bound in its scope a


def fresh(x, avoid):
    """x1, x2, ...: the first variant of x not in avoid."""
    k = 1
    while f"{x}{k}" in avoid:
        k += 1
    return f"{x}{k}"


def subst(e, x, t):
    """e[t/x]: replace the free occurrences of x by t, renaming a bound variable that
    would capture a variable of t."""
    match e:
        case Var(y):
            return t if y == x else e
        case Fun(f, args):
            return Fun(f, tuple(subst(a, x, t) for a in args))
        case Pred(p, args):
            return Pred(p, tuple(subst(a, x, t) for a in args))
        case Bot():
            return e
        case Not(a):
            return Not(subst(a, x, t))
        case And(a, b) | Or(a, b) | Imp(a, b):
            return type(e)(subst(a, x, t), subst(b, x, t))
        case Forall(y, a) | Exists(y, a):
            if y == x or x not in free(a):
                return e  # no free x below: nothing to replace
            if y in free(t):  # y would capture t's y: rename it first
                z = fresh(y, free(t) | free(a) | {x})
                a, y = subst(a, y, Var(z)), z
            return type(e)(y, subst(a, x, t))


TOKEN = re.compile(r"\s*(->|[A-Za-z_][A-Za-z0-9_']*|[()~&|.,=])")


def parse(text):
    """~ not, & and, | or, -> implies (to the right), forall x. and exists x. as far
    right as possible, false, P(t, ...) and t = u; x, y, z, u, v, w are variables."""
    tokens = TOKEN.findall(text)
    assert "".join(tokens) == re.sub(r"\s", "", text), f"cannot read {text!r}"
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take(expected=None):
        nonlocal pos
        tok = tokens[pos]
        assert expected in (None, tok), f"expected {expected!r}, found {tok!r}"
        pos += 1
        return tok

    def arguments():  # (t1, ..., tn), or nothing
        if peek() != "(":
            return ()
        take("(")
        args = [term()]
        while peek() == ",":
            take(",")
            args.append(term())
        take(")")
        return tuple(args)

    def term():
        name = take()
        if peek() == "(":
            return Fun(name, arguments())
        return Var(name) if VARIABLE.match(name) else Fun(name)

    def formula():  # implication, the loosest
        left = disjunction()
        if peek() == "->":
            take()
            return Imp(left, formula())
        return left

    def disjunction():
        left = conjunction()
        while peek() == "|":
            take()
            left = Or(left, conjunction())
        return left

    def conjunction():
        left = unary()
        while peek() == "&":
            take()
            left = And(left, unary())
        return left

    def unary():
        tok = peek()
        if tok == "~":
            take()
            return Not(unary())
        if tok in ("forall", "exists"):
            take()
            x = take()
            take(".")
            return (Forall if tok == "forall" else Exists)(x, formula())
        if tok == "(":
            take()
            inner = formula()
            take(")")
            return inner
        if tok == "false":
            take()
            return Bot()
        if tok[0].isupper():
            name = take()
            return Pred(name, arguments())
        left = term()
        take("=")
        return Pred("=", (left, term()))

    result = formula()
    assert pos == len(tokens), f"unexpected {tokens[pos]!r}"
    return result


def show(e, outer=0):
    """Print with the brackets the priorities need: -> 1, | 2, & 3, prefix 4."""
    match e:
        case Var(x):
            return x
        case Fun(f, ()):
            return f
        case Fun(f, args):
            return f"{f}({', '.join(show(a) for a in args)})"
        case Pred("=", (a, b)):
            text, level = f"{show(a)} = {show(b)}", 4
        case Pred(p, ()):
            return p
        case Pred(p, args):
            return f"{p}({', '.join(show(a) for a in args)})"
        case Bot():
            return "false"
        case Not(a):
            text, level = "~" + show(a, 4), 4
        case And(a, b):
            text, level = f"{show(a, 3)} & {show(b, 4)}", 3
        case Or(a, b):
            text, level = f"{show(a, 2)} | {show(b, 3)}", 2
        case Imp(a, b):
            text, level = f"{show(a, 2)} -> {show(b, 1)}", 1
        case Forall(x, a) | Exists(x, a):
            word = "forall" if isinstance(e, Forall) else "exists"
            text, level = f"{word} {x}. {show(a)}", 0  # its scope runs to the right
    return f"({text})" if level < outer else text
