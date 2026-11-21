"""evaluate.py: five rules about the library, checked on the town's tables."""
from formulas import parse
from structures import town

RULES = [
    ("a person with a book out is a member",
     "forall x. (exists y. Out(x, y)) -> Member(x)"),
    ("a book is out to one person at most",
     "forall y. forall x. Out(x, y) -> forall z. Out(z, y) -> z = x"),
    ("what is out has been borrowed",
     "forall x. forall y. Out(x, y) -> Borrowed(x, y)"),
    ("every book has been borrowed",
     "forall y. Book(y) -> exists x. Borrowed(x, y)"),
    ("every member has a friend",
     "forall x. Member(x) -> exists y. Friend(x, y)"),
]

A = town()
print(f"{len(A.domain)} elements; {len(A.relations['Out'])} loans out now")
for words, text in RULES:
    A.atoms = 0
    bad = A.counterexamples(parse(text))
    print(f"{words}: {'holds' if not bad else 'fails'} ({A.atoms} atoms evaluated)")
    for vals in bad[:3]:
        print("   counterexample:", ", ".join(vals))
    if len(bad) > 3:
        print(f"   ... {len(bad)} in all")
