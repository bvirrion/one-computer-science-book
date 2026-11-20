"""exo_failure.py: the failure function of aabaaab."""
from kmp import failure

pattern = "aabaaab"
pi = failure(pattern)
print(" ".join(f"pi[{q}]={pi[q]}" for q in range(1, len(pattern) + 1)))
