"""exo_forall_bug.py: a proof that the checker refuses."""
from checker import ProofError, check
from checker import step as s

HYPOTHESES = ["forall x. Member(x) -> MayBorrow(x)", "Member(y)"]
PROOF = s("forall_i", "forall x. MayBorrow(x)",
          s("imp_e", "MayBorrow(y)",
            s("forall_e", "Member(y) -> MayBorrow(y)",
              s("hyp", "forall x. Member(x) -> MayBorrow(x)"), term="y"),
            s("hyp", "Member(y)")),
          term="y")
try:
    print(check(PROOF, HYPOTHESES), "steps checked")
except ProofError as error:
    print("rejected:", error)
