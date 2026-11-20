"""check_demo.py: five proofs given to the checker."""
from checker import ProofError, check
from formulas import show
from proofs import ALL, MODUS_PONENS, NO_COUNTEREXAMPLE, SYLLOGISM, WRONG_ALL

for hypotheses, proof in [MODUS_PONENS, SYLLOGISM, NO_COUNTEREXAMPLE, ALL, WRONG_ALL]:
    print(", ".join(hypotheses), "|-", show(proof.goal))
    try:
        print(f"   accepted: {check(proof, hypotheses)} steps checked")
    except ProofError as error:
        print(f"   rejected: {error}")
