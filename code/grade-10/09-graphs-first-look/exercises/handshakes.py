"""Problem: the largest friendship component, with and without its bridges."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "lib"))
from given_graphs import components, distances  # noqa: E402
from load_friends import load_friends  # noqa: E402

PATH = Path(__file__).parent.parent / "listings" / "friendships.csv"


def eccentricities(g):
    largest = components(g)[0]
    return {v: max(distances(g, v).values()) for v in largest}


def summary(g):
    ecc = eccentricities(g)
    radius = min(ecc.values())
    centre = sorted(v for v in ecc if ecc[v] == radius)
    return len(ecc), radius, max(ecc.values()), centre


if __name__ == "__main__":
    g = load_friends(PATH)
    print("largest component, radius, diameter, centre:", summary(g))
    for a, b in [(1, 28), (5, 37), (12, 20)]:
        g[a].discard(b)
        g[b].discard(a)
        sizes = [len(p) for p in components(g)]
        print(f"without {a}-{b}: components {sizes}, summary {summary(g)}")
        g[a].add(b)
        g[b].add(a)
