class DFlipFlop:
    """Copies its input D to its output Q at a rising edge of the clock, only then."""

    def __init__(self):
        self.q = 0
        self.clock = 0

    def update(self, d, clock):
        if self.clock == 0 and clock == 1:  # rising edge
            self.q = d
        self.clock = clock


register = [DFlipFlop() for _ in range(4)]  # a 4-bit register
inputs = [0b0101, 0b0101, 0b1100, 0b1100, 0b1111, 0b0011, 0b0011, 0b1000]
clocks = [0, 1, 1, 0, 0, 1, 0, 1]
for t, (d, clock) in enumerate(zip(inputs, clocks)):
    for i, ff in enumerate(register):
        ff.update((d >> i) & 1, clock)
    q = sum(ff.q << i for i, ff in enumerate(register))
    print(f"t={t}  D={d:04b}  clock={clock}  Q={q:04b}")
