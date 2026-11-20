"""btfn.py: backward taken, forward not taken, a static predictor (exercise 7)."""
from rv import decode


class BackwardTaken:
    """Predict taken exactly for the branches that jump backwards: loop branches."""
    name = "backward taken"

    def __init__(self, steps):
        self.back = {s.pc: decode(s.word).imm < 0 for s in steps if s.kind == "branch"}

    def predict(self, pc):
        return self.back[pc]

    def update(self, pc, taken):
        pass
