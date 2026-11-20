"""seq.py: gates that may feed back, each taking one time unit (latches and flip-flops);
a combinational circuit (as in chapter 27); minimal sums of products; and a clocked
synchronous circuit, its state held in D flip-flops."""

from itertools import combinations, product

OPS = {
    "NOT": lambda xs: 1 - xs[0],
    "AND": lambda xs: int(all(xs)),
    "OR": lambda xs: int(any(xs)),
    "XOR": lambda xs: sum(xs) % 2,
    "NAND": lambda xs: 1 - int(all(xs)),
    "NOR": lambda xs: 1 - int(any(xs)),
}


class Net:
    """Gates wired in any way, loops allowed. At each time unit every gate's output
    becomes its function of the values its inputs had one unit before."""

    def __init__(self, *inputs):
        self.inputs = list(inputs)
        self.gates = {}  # output wire -> (op, input wires)

    def gate(self, wire, op, *ins):
        self.gates[wire] = (op, ins)
        return wire

    def tick(self, v):
        """v: the value of every wire now. Returns the values one time unit later."""
        new = dict(v)
        for wire, (op, ins) in self.gates.items():
            new[wire] = OPS[op]([v[i] for i in ins])
        return new


class Circuit:
    """A combinational circuit: gates added in topological order (chapter 27)."""

    def __init__(self, *inputs):
        self.inputs, self.gates, self.outputs = list(inputs), [], {}

    def gate(self, op, *ins):
        wire = f"w{len(self.gates)}"
        self.gates.append((wire, op, ins))
        return wire

    def evaluate(self, values):
        v = dict(values)
        for wire, op, ins in self.gates:
            v[wire] = OPS[op]([v[i] for i in ins])
        return {name: v[w] for name, w in self.outputs.items()}


def minimal_sop(ones, dont_care, n):
    """A minimal sum of products of an n-variable function, as terms like '1-0'
    (variable i is 1, absent, 0): prime implicants, then the smallest cover."""
    terms = {format(m, f"0{n}b") for m in set(ones) | set(dont_care)}
    primes = set()
    while terms:
        merged, used = set(), set()
        for s, t in combinations(sorted(terms), 2):
            diff = [i for i in range(n) if s[i] != t[i]]
            if len(diff) == 1 and "-" not in (s[diff[0]], t[diff[0]]):
                merged.add(s[:diff[0]] + "-" + s[diff[0] + 1:])
                used |= {s, t}
        primes |= terms - used
        terms = merged
    need = [format(m, f"0{n}b") for m in ones]
    hits = {p: {m for m in need if all(a in "-" + b for a, b in zip(p, m))}
            for p in primes}
    for k in range(len(primes) + 1):  # the fewest products, then the fewest literals
        best = [c for c in combinations(sorted(primes), k)
                if set().union(*(hits[p] for p in c)) == set(need)]
        if best:
            literals = [sum(len(p) - p.count("-") for p in c) for c in best]
            return sorted(best[literals.index(min(literals))])
    return []


def sop_value(terms, bits):
    return int(any(all(t == "-" or int(t) == b for t, b in zip(term, bits))
                   for term in terms))


def sop_text(terms, names):
    if not terms:
        return "0"
    if terms == ["-" * len(names)]:
        return "1"
    return " + ".join("".join(x + ("'" if t == "0" else "") for t, x in zip(term, names)
                              if t != "-") for term in terms)


def sop_gates(equations):
    """Gate count of two-level logic: a NOT per complemented variable, an AND per
    product of two literals or more, an OR per sum of two products or more."""
    negated, ands, ors = set(), 0, 0
    for terms in equations:
        for term in terms:
            negated |= {i for i, t in enumerate(term) if t == "0"}
            ands += len(term) - term.count("-") >= 2
        ors += len(terms) >= 2
    return len(negated) + ands + ors


def all_words(alphabet, longest):
    for k in range(longest + 1):
        yield from product(alphabet, repeat=k)
