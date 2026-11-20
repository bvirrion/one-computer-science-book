"""ram.py: a 16 x 4 random-access memory from a decoder, 64 one-bit cells (D latches)
and four 16-to-1 multiplexers, the decoder and multiplexers as gate circuits."""

from seq import Circuit


def decoder(k):
    """k address bits in, 2^k outputs, exactly one of them 1."""
    c = Circuit(*[f"a{i}" for i in range(k)])
    inv = [c.gate("NOT", f"a{i}") for i in range(k)]
    for row in range(2 ** k):
        lits = [f"a{i}" if row >> i & 1 else inv[i] for i in range(k)]
        c.outputs[row] = c.gate("AND", *lits)
    return c


def multiplexer(k):
    """2^k data inputs, k select inputs: a tree of 2-to-1 multiplexers."""
    c = Circuit(*[f"x{j}" for j in range(2 ** k)], *[f"a{i}" for i in range(k)])
    level = [f"x{j}" for j in range(2 ** k)]
    for i in range(k):
        s, s_inv = f"a{i}", c.gate("NOT", f"a{i}")
        level = [c.gate("OR", c.gate("AND", s_inv, x0), c.gate("AND", s, x1))
                 for x0, x1 in zip(level[::2], level[1::2])]
    c.outputs["out"] = level[0]
    return c


class RAM:
    LATCH_GATES = 5  # a D latch: NOT, two ANDs, two NORs

    def __init__(self, k=4, width=4):
        self.k, self.width = k, width
        self.cells = [[0] * width for _ in range(2 ** k)]
        self.dec, self.mux = decoder(k), multiplexer(k)

    def address(self, a):
        return {f"a{i}": a >> i & 1 for i in range(self.k)}

    def write(self, a, data):
        rows = self.dec.evaluate(self.address(a))
        for row, selected in rows.items():  # a cell's enable: write AND its row
            if selected:
                self.cells[row] = [data >> b & 1 for b in range(self.width)]

    def read(self, a):
        bits = []
        for b in range(self.width):  # one multiplexer per bit of the word
            data = {f"x{j}": self.cells[j][b] for j in range(2 ** self.k)}
            bits.append(self.mux.evaluate(data | self.address(a))["out"])
        return sum(bit << b for b, bit in enumerate(bits))

    def gates(self):
        n = 2 ** self.k
        return {"decoder": len(self.dec.gates), "write enables": n,
                "cells": n * self.width * self.LATCH_GATES,
                "read multiplexers": self.width * len(self.mux.gates)}


if __name__ == "__main__":
    ram = RAM()
    for a, v in [(3, 9), (12, 5), (3, 14)]:
        ram.write(a, v)
        print(f"write {v:2} at address {a:2}")
    print("read:", ", ".join(f"[{a}] = {ram.read(a)}" for a in (3, 12, 7)))
    g = ram.gates()
    print("gates:", ", ".join(f"{k} {v}" for k, v in g.items()) + ";",
          "total", sum(g.values()))
