"""exo_is_flow.py: three candidate flows on the network of flow.py."""
CAP = {("s", "a"): 8, ("s", "b"): 6, ("a", "c"): 7, ("a", "d"): 5, ("b", "c"): 6,
       ("c", "t"): 7, ("d", "t"): 9}  # the network of flow.py
CANDIDATES = {
    "f1": {"sa": 7, "sb": 5, "ac": 5, "ad": 2, "bc": 5, "ct": 7, "dt": 2},
    "f2": {"sa": 8, "sb": 6, "ac": 3, "ad": 5, "bc": 6, "ct": 9, "dt": 5},
    "f3": {"sa": 6, "sb": 6, "ac": 1, "ad": 5, "bc": 6, "ct": 7, "dt": 5},
}
for name, f in CANDIDATES.items():
    flow = {(e[0], e[1]): x for e, x in f.items()}
    over = [u + v for (u, v), x in flow.items() if x > CAP[(u, v)]]
    unbalanced = [w for w in "abcd"
                  if sum(x for (u, v), x in flow.items() if v == w)
                  != sum(x for (u, v), x in flow.items() if u == w)]
    value = sum(x for (u, v), x in flow.items() if u == "s")
    print(f"{name}: over capacity {over}, not conserved at {unbalanced}, value {value}")
