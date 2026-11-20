"""adders.py: an n-bit ripple-carry adder and a carry-lookahead adder in blocks of four,
checked against integer addition on every input, with their sizes and delays."""

from circuit import Circuit, bits


def full_adder(c, a, b, cin):
    p = c.gate("XOR", a, b)
    s = c.gate("XOR", p, cin)
    cout = c.gate("OR", c.gate("AND", a, b), c.gate("AND", p, cin))
    return s, cout


def ripple(n):
    c = Circuit(*[f"a{i}" for i in range(n)], *[f"b{i}" for i in range(n)], "c0")
    carry = "c0"
    for i in range(n):
        c.outputs[f"s{i}"], carry = full_adder(c, f"a{i}", f"b{i}", carry)
    c.outputs["cout"] = carry
    return c


def lookahead_block(c, a, b, cin):
    """Four bits: c_{i+1} = g_i + p_i g_{i-1} + ... + p_i ... p_0 c_0, two levels."""
    g = [c.gate("AND", x, y) for x, y in zip(a, b)]
    p = [c.gate("XOR", x, y) for x, y in zip(a, b)]
    carries = [cin]
    for i in range(4):
        terms = [g[i]]
        for j in range(i - 1, -2, -1):  # g_j (or c_0) carried through p_{j+1} ... p_i
            src = g[j] if j >= 0 else cin
            terms.append(c.gate("AND", src, *p[j + 1:i + 1]))
        carries.append(c.gate("OR", *terms))
    sums = [c.gate("XOR", p[i], carries[i]) for i in range(4)]
    return sums, carries[4]


def lookahead(n):
    c = Circuit(*[f"a{i}" for i in range(n)], *[f"b{i}" for i in range(n)], "c0")
    carry = "c0"
    for k in range(0, n, 4):  # blocks of four, the carries rippling between blocks
        sums, carry = lookahead_block(c, [f"a{i}" for i in range(k, k + 4)],
                                      [f"b{i}" for i in range(k, k + 4)], carry)
        for i, s in enumerate(sums):
            c.outputs[f"s{k + i}"] = s
    c.outputs["cout"] = carry
    return c


def correct(c, n):
    for x in range(2 ** n):
        for y in range(2 ** n):
            for c0 in (0, 1):
                values = {f"a{i}": v for i, v in enumerate(bits(x, n))}
                values |= {f"b{i}": v for i, v in enumerate(bits(y, n))}
                out = c.evaluate(values | {"c0": c0})
                total = sum(out[f"s{i}"] << i for i in range(n)) + (out["cout"] << n)
                if total != x + y + c0:
                    return False
    return True


if __name__ == "__main__":
    for n in (4, 8):
        for name, build in (("ripple-carry", ripple), ("lookahead", lookahead)):
            c = build(n)
            print(f"{n} bits, {name:12}: {c.size():3} gates, delay {c.delay():2},"
                  f" all {2 ** (2 * n + 1)} sums correct: {correct(c, n)}")
    for n in (16, 32, 64):
        print(f"{n} bits: delay {ripple(n).delay():3} rippling,"
              f" {lookahead(n).delay():2} with lookahead blocks")
