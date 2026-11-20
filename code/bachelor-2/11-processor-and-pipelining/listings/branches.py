"""branches.py: three predictors on the branch traces of three programs."""
from pipeline import steps_of
from predictor import NotTaken, OneBit, TwoBit, mispredictions

PROGRAMS = ["loop_sum.S", "bubble_sort.S", "collatz.S"]

print(f"{'program':<15}{'branches':>9}{'taken':>7}   mispredicted: "
      f"{'not taken':>10}{'one-bit':>9}{'two-bit':>9}")
for name in PROGRAMS:
    with open(name) as f:
        steps = steps_of(f.read())
    trace = [(s.pc, s.branch_taken) for s in steps if s.kind == "branch"]
    taken = sum(t for _, t in trace)
    wrong = [mispredictions(trace, p()) for p in (NotTaken, OneBit, TwoBit)]
    columns = "".join(f"{w:>9}" for w in wrong)
    print(f"{name:<15}{len(trace):>9}{taken:>7}" + " " * 17 + columns)
