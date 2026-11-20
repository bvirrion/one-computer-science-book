"""exo_proofs.py: the proofs of exercises 7, 10 and 11, given to the checker."""
from checker import ProofError, check
from exists_rules import EXISTS
from formulas import show
from proofs_more import CONVERSE, DE_MORGAN, EXCLUDED_MIDDLE, SWAP

for hypotheses, proof in [DE_MORGAN, SWAP, CONVERSE, EXCLUDED_MIDDLE]:
    print(", ".join(hypotheses), "|-", show(proof.goal))
    try:
        print(f"   accepted: {check(proof, hypotheses, EXISTS)} steps checked")
    except ProofError as error:
        print(f"   rejected: {error}")
