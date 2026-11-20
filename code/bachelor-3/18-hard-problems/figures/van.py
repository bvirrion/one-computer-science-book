"""Write the data of the delivery-van map: the 12 places (km), the minimum spanning tree
as segments, the tree-doubling tour and the optimal tour, from listings/tsp.py."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))
from tsp import held_karp, minimum_spanning_tree, town_places, tree_doubling  # noqa: E402


def xy(p):
    return f"{p[1] / 1000:.3f} {p[2] / 1000:.3f}\n"


def main() -> None:
    van = town_places()[:12]
    (HERE / "van_places.dat").write_text("x y\n" + "".join(xy(p) for p in van))
    children = minimum_spanning_tree(van)
    segments = "".join(xy(van[u]) + xy(van[v]) + "\n"
                       for u in children for v in children[u])
    (HERE / "van_mst.dat").write_text("x y\n" + segments)
    for name, tour in (("doubling", tree_doubling(van)), ("optimum", held_karp(van))):
        (HERE / f"van_{name}.dat").write_text(
            "x y\n" + "".join(xy(van[i]) for i in tour + tour[:1]))


if __name__ == "__main__":
    main()
