"""puzzle.py: four friends, three rules: who can come to dinner?"""

from evaluate import models
from formula import Var
from normal_forms import cnf, show_sets
from quine import quine

ana, ben, cyd, dee = Var("ana"), Var("ben"), Var("cyd"), Var("dee")
rules = [ana >> ben,                   # Ana comes only if Ben comes
         ~(ben & cyd),                 # Ben and Cyd will not both come
         (cyd | dee) & (dee >> ana)]   # Cyd or Dee comes; Dee only with Ana
dinner = rules[0] & rules[1] & rules[2]
clauses = cnf(dinner)

if __name__ == "__main__":
    print("formula:", dinner)
    for v in models(dinner):
        print("model:", ", ".join(name for name in v if v[name]))
    print("CNF:", show_sets(clauses, "&", "|"))
    stats = {"nodes": 0}
    model = quine(clauses, stats)
    print("Quine's algorithm:", sorted(model), "after", stats["nodes"], "nodes")
    everyone = dinner & ana & ben & cyd & dee
    print("everyone comes:", models(everyone) or "no model")
