"""pipeline.py: a timing model of the five-stage pipeline, run on rv's step records."""
from dataclasses import dataclass, field

from predictor import NotTaken
from rv import Machine

# How many cycles after the producer's EX a consumer may be in EX:
LOAD_DELAY, ALU_DELAY, NO_FORWARD_DELAY = 2, 1, 3


def steps_of(text, inputs=()):
    """The dynamic instruction stream: one rv Step per executed instruction."""
    m = Machine(text, inputs=list(inputs))
    steps = []
    m.run(trace=steps.append)
    return steps


@dataclass
class Timing:
    fetch: list = field(default_factory=list)    # cycle of IF, per instruction
    decode: list = field(default_factory=list)   # cycle it enters ID
    execute: list = field(default_factory=list)  # cycle of EX (MEM and WB follow)
    stalls: int = 0                              # cycles held in ID by a data hazard
    flushed: int = 0                             # cycles lost to branches and jumps
    mispredicted: int = 0

    @property
    def cycles(self):
        return self.execute[-1] + 2  # the last WB

    def cpi(self):
        return self.cycles / len(self.execute)


def schedule(steps, forwarding=True, predictor=None):
    """The cycle of every stage of every instruction, the first IF in cycle 1."""
    predictor = predictor or NotTaken()
    t = Timing()
    ready = {}                       # register -> earliest EX of a reader
    next_fetch, prev_ex = 1, 1
    for s in steps:
        f = next_fetch
        d = max(f + 1, prev_ex)      # ID frees when the one ahead enters EX
        need = max([ready.get(r, 0) for r in s.srcs], default=0)
        x = max(d + 1, need)         # the hazard check, made in ID
        if t.execute:
            t.flushed += d - prev_ex     # fetched late: a branch or a jump
            t.stalls += x - (d + 1)      # held in ID until operands are ready
        t.fetch.append(f)
        t.decode.append(d)
        t.execute.append(x)
        if s.rd is not None:
            if not forwarding:           # read in ID once WB has written it
                ready[s.rd] = x + NO_FORWARD_DELAY
            else:
                ready[s.rd] = x + (LOAD_DELAY if s.kind == "load" else ALU_DELAY)
        next_fetch = d               # the next is fetched as this enters ID
        if s.kind == "branch":
            guess = predictor.predict(s.pc)
            predictor.update(s.pc, s.branch_taken)
            if guess != s.branch_taken:  # resolved in EX: fetch again after it
                t.mispredicted += 1
                next_fetch = x + 1
        elif s.kind == "jump":
            jal = s.text.split()[0] == "jal"   # jal: target known in ID; jalr: EX
            next_fetch = d + 1 if jal else x + 1
        prev_ex = x
    return t


if __name__ == "__main__":
    import sys
    from predictor import TwoBit
    with open(sys.argv[1]) as f:
        steps = steps_of(f.read())
    for label, fwd, pred in [("no forwarding", False, None), ("forwarding", True, None),
                             ("forwarding + two-bit", True, TwoBit())]:
        t = schedule(steps, fwd, pred)
        print(f"{label:<21} {len(steps)} instr. {t.cycles:>6} cycles  CPI {t.cpi():.2f}"
              f"  stalls {t.stalls:>4}  flushed {t.flushed:>4}")
