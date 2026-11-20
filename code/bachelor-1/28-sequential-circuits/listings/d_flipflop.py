"""d_flipflop.py: an edge-triggered D flip-flop from two D latches (master and slave),
simulated gate by gate; its timing diagram, and its setup, hold and clock-to-output
times found by moving the change of D around the clock edge."""

from pathlib import Path

from seq import Net


def d_latch(n, name, d, enable):
    """S = D and E, R = D' and E, into an SR latch of two NOR gates."""
    n.gate(name + "d'", "NOT", d)
    n.gate(name + "s", "AND", d, enable)
    n.gate(name + "r", "AND", name + "d'", enable)
    n.gate(name + "Q", "NOR", name + "r", name + "Q'")
    n.gate(name + "Q'", "NOR", name + "s", name + "Q")
    return name + "Q"


def d_flipflop():
    n = Net("clk", "D")
    n.gate("clk'", "NOT", "clk")
    d_latch(n, "m", "D", "clk'")  # the master follows D while the clock is 0
    d_latch(n, "s", "mQ", "clk")  # the slave copies the master while it is 1
    return n


def simulate(clock, data):
    """clock, data: the input at each time unit. Returns Q at each time unit."""
    n = d_flipflop()
    v = {w: 0 for w in n.gates} | {"mQ'": 1, "sQ'": 1, "clk": 0, "D": 0}
    for _ in range(10):  # settle with clk = D = 0
        v = n.tick(v)
    q = []
    for c, d in zip(clock, data):
        v = n.tick(v | {"clk": c, "D": d})
        q.append(v["sQ"])
    return q


def clock(units, half):
    return [(t // half) % 2 for t in range(units)]


def stored(offset, old, half=10):
    """D goes from old to 1 - old at edge + offset, the rising edge being at 3 * half.
    Returns the value the flip-flop holds after the edge."""
    edge = 3 * half
    data = [old if t < edge + offset else 1 - old for t in range(4 * half)]
    return simulate(clock(4 * half, half), data)[-1]


if __name__ == "__main__":
    clk = clock(80, 10)
    d = [int(5 <= t < 25 or 46 <= t < 53 or 57 <= t < 63) for t in range(80)]
    q = simulate(clk, d)
    rows = {"clk": clk, "D": d, "Q": q}
    for name, wave in rows.items():
        print(f"{name:4}" + "".join("-" if b else "_" for b in wave))
    with open(Path(__file__).resolve().parents[1] / "figures" / "dff.dat", "w") as f:
        f.write("t clk D Q\n")
        for t in range(80):
            f.write(f"{t} {clk[t]} {d[t]} {q[t]}\n")
    wrong = []  # changes after which the flip-flop misses D's value at the edge
    for old in (0, 1):
        got = [stored(k, old) for k in range(-4, 5)]
        print(f"D goes {old} -> {1 - old} at edge + k, k = -4..4; stored:", *got)
        wrong += [k for k, b in zip(range(-4, 5), got)
                  if b != (1 - old if k <= 0 else old)]
    print(f"setup time {1 - min(wrong)} units, hold time {max(wrong)} units")
    q = simulate(clock(40, 10), [int(t >= 20) for t in range(40)])
    print("clock edge to Q:", q.index(1) - 30, "time units")
