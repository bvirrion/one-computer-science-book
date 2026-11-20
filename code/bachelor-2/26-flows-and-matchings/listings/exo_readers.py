"""exo_readers.py: 40 readers and 8 reading-room slots; reader k can come to the slots
k mod 8, 3k mod 8 and (5k + 1) mod 8."""
from maxflow import Network, max_flow, min_cut

READERS = range(1, 41)


def available(k):
    return sorted({k % 8, 3 * k % 8, (5 * k + 1) % 8})


for seats in [[5] * 8, [2, 2, 5, 5, 6, 6, 7, 7]]:
    net = Network()
    for k in READERS:
        net.add_edge("s", ("r", k), 1)
        for slot in available(k):
            net.add_edge(("r", k), ("slot", slot), 1)
    for slot, n in enumerate(seats):
        net.add_edge(("slot", slot), "t", n)
    value, flow = max_flow(net, "s", "t")
    print(f"seats {seats}, {sum(seats)} in all: {value} of {len(READERS)} placed")
    if value < len(READERS):
        side, _ = min_cut(net, flow, "s")
        stuck = [k for k in READERS if ("r", k) in side]
        slots = sorted({s for k in stuck for s in available(k)})
        print(f"   readers {stuck} can only use slots {slots},",
              f"{sum(seats[s] for s in slots)} seats")
