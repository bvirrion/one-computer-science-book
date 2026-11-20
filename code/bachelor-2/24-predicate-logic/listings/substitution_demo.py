"""substitution_demo.py: substituting y for x in "x has a successor", in Z/5."""
from formulas import Var, free, parse, show, subst
from structures import Structure

phi = parse("exists y. y = s(x)")  # true whatever x is
captured = parse("exists y. y = s(y)")  # replacing the x by y, naively
renamed = subst(phi, "x", Var("y"))  # the bound y is renamed first
A = Structure(range(5), {}, {"s": lambda a: (a + 1) % 5})  # the successor modulo 5
for name, f in [("phi", phi), ("naive", captured), ("phi[y/x]", renamed)]:
    values = [A.holds(f, {"x": d, "y": d}) for d in A.domain]
    print(f"{name:9} {show(f):22} free: {sorted(free(f))}  true for 0..4: {values}")
