"""library.py: consequences of the library's rules, proved and checked; a
countermodel for a rule that does not follow."""
import itertools

from checker import check
from checker import step as s
from formulas import parse
from structures import Structure

H1 = "forall x. forall y. Out(x, y) -> Member(x)"
H2 = "forall x. Member(x) -> MayBorrow(x)"
H3 = "forall x. forall y. Out(x, y) -> Borrowed(x, y)"
RULES = [H1, H2, H3]


def out_member():  # Out(x, y) |- Member(x), from H1
    return s("imp_e", "Member(x)",
             s("forall_e", "Out(x, y) -> Member(x)",
               s("forall_e", "forall y. Out(x, y) -> Member(x)", s("hyp", H1),
                 term="x"),
               term="y"),
             s("hyp", "Out(x, y)"))


C1 = s("forall_i", "forall x. forall y. Out(x, y) -> MayBorrow(x)",
       s("forall_i", "forall y. Out(x, y) -> MayBorrow(x)",
         s("imp_i", "Out(x, y) -> MayBorrow(x)",
           s("imp_e", "MayBorrow(x)",
             s("forall_e", "Member(x) -> MayBorrow(x)", s("hyp", H2), term="x"),
             out_member())),
         term="y"),
       term="x")

C2 = s("forall_i", "forall x. forall y. Out(x, y) -> Member(x) & Borrowed(x, y)",
       s("forall_i", "forall y. Out(x, y) -> Member(x) & Borrowed(x, y)",
         s("imp_i", "Out(x, y) -> Member(x) & Borrowed(x, y)",
           s("and_i", "Member(x) & Borrowed(x, y)",
             out_member(),
             s("imp_e", "Borrowed(x, y)",
               s("forall_e", "Out(x, y) -> Borrowed(x, y)",
                 s("forall_e", "forall y. Out(x, y) -> Borrowed(x, y)", s("hyp", H3),
                   term="x"),
                 term="y"),
               s("hyp", "Out(x, y)")))),
         term="y"),
       term="x")

C3 = s("forall_i", "forall x. ~MayBorrow(x) -> ~Member(x)",
       s("imp_i", "~MayBorrow(x) -> ~Member(x)",
         s("not_i", "~Member(x)",
           s("not_e", "false",
             s("imp_e", "MayBorrow(x)",
               s("forall_e", "Member(x) -> MayBorrow(x)", s("hyp", H2), term="x"),
               s("hyp", "Member(x)")),
             s("hyp", "~MayBorrow(x)")))),
       term="x")

total = 0
for name, proof in [("C1", C1), ("C2", C2), ("C3", C3)]:
    steps = check(proof, RULES)
    total += steps
    print(f"{name} proved from the rules, {steps} steps checked")
print(f"in all: 3 consequences, {total} steps")

C4 = parse("forall x. Member(x) -> exists y. Out(x, y)")  # every member has a book out


def relations(arity):
    """Every relation of this arity on {0, 1}: every set of tuples."""
    cells = list(itertools.product([0, 1], repeat=arity))
    subsets = (itertools.combinations(cells, k) for k in range(len(cells) + 1))
    return [set(c) for group in subsets for c in group]


tried = 0
for out, borrowed, member, may in itertools.product(relations(2), relations(2),
                                                     relations(1), relations(1)):
    A = Structure([0, 1], {"Out": out, "Borrowed": borrowed, "Member": member,
                           "MayBorrow": may})
    tried += 1
    if all(A.holds(parse(h)) for h in RULES) and not A.holds(C4):
        print(f"C4 does not follow: structure {tried} of 4096 on {{0, 1}} is a model")
        print(f"   of the rules, Member = {sorted(member)}, MayBorrow = {sorted(may)},")
        print(f"   Out = {sorted(out)}, Borrowed = {sorted(borrowed)}; C4 is false")
        break
