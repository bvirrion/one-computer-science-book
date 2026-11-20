"""cost.py: atoms evaluated for transitivity, three nested quantifiers, as |D| grows."""
from formulas import parse
from structures import Structure

phi = parse("forall x. forall y. forall z. R(x, y) & R(y, z) -> R(x, z)")
print(" |D|     |D|^3      atoms  atoms/|D|^3  holds")
for n in [10, 20, 40, 80]:
    less = {(a, b) for a in range(n) for b in range(n) if a < b}
    A = Structure(range(n), {"R": less})
    ok = A.holds(phi)
    print(f"{n:4} {n ** 3:9} {A.atoms:10} {A.atoms / n ** 3:12.2f}  {ok}")
