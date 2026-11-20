"""hall.py: no perfect matching? The minimum cut names a set of readers with too few
slots between them (Hall's condition fails)."""
from maxflow import Network, max_flow, min_cut

ADJ = {"Ada": ["Mon", "Tue"], "Ben": ["Mon"], "Cy": ["Tue", "Wed", "Thu"],
       "Dee": ["Wed", "Fri"], "Eve": ["Mon", "Wed"], "Fay": ["Mon", "Tue"]}
SLOTS = sorted({v for slots in ADJ.values() for v in slots})
net = Network()
for u, slots in ADJ.items():
    net.add_edge("s", u, 1)
    for v in slots:
        net.add_edge(u, v, len(ADJ))  # "infinite": more than any cut through s
for v in SLOTS:
    net.add_edge(v, "t", 1)
value, flow = max_flow(net, "s", "t")
side, _ = min_cut(net, flow, "s")
readers = sorted(u for u in ADJ if u in side)
slots = sorted({v for u in readers for v in ADJ[u]})
print(f"{len(ADJ)} readers, {len(SLOTS)} slots, at most {value} matched")
print(f"the readers {readers} accept only the {len(slots)} slots {slots}")
