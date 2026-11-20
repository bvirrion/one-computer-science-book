"""circuit.py: a combinational circuit as a directed acyclic graph of gates; evaluation
in the order the gates were added, which is topological; delay as the longest path."""

OPS = {
    "NOT": lambda xs: 1 - xs[0],
    "AND": lambda xs: int(all(xs)),
    "OR": lambda xs: int(any(xs)),
    "XOR": lambda xs: sum(xs) % 2,
    "NAND": lambda xs: 1 - int(all(xs)),
    "NOR": lambda xs: 1 - int(any(xs)),
}


class Circuit:
    def __init__(self, *inputs):
        self.inputs = list(inputs)
        self.gates = []  # (wire, op, input wires), in the order added
        self.outputs = {}

    def gate(self, op, *ins):
        """Add a gate whose inputs are existing wires; return its output wire."""
        known = set(self.inputs) | {w for w, _, _ in self.gates}
        assert all(i in known for i in ins), "a gate may only use existing wires"
        wire = f"w{len(self.gates)}"
        self.gates.append((wire, op, ins))
        return wire

    def evaluate(self, values):
        """values: input wire -> 0 or 1. Returns the value of every output."""
        v = dict(values)
        for wire, op, ins in self.gates:  # every input is computed before
            v[wire] = OPS[op]([v[i] for i in ins])
        return {name: v[w] for name, w in self.outputs.items()}

    def delay(self):
        """The longest path from an input to an output, counted in gates."""
        depth = {i: 0 for i in self.inputs}
        for wire, _, ins in self.gates:
            depth[wire] = 1 + max((depth[i] for i in ins), default=0)
        return max(depth[w] for w in self.outputs.values())

    def size(self):
        return len(self.gates)


def bits(n, width):
    """The bits of n, least significant first."""
    return [(n >> i) & 1 for i in range(width)]
