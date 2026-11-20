"""Write the chapter's figure files from the code: the k-d tree's partition, Lloyd's
iterations, the single-linkage dendrogram and the depth chart's data."""
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))

from dataset import blobs  # noqa: E402
from hac import NAMES, PTS, hac  # noqa: E402
from kdtree import build  # noqa: E402
from kmeans import assign, centroid, lloyd  # noqa: E402

HEAD = "% written by figs.py; do not edit\n"


def kd_partition():
    """Splitting segments of a k-d tree of 15 points in [0, 10] x [0, 10]."""
    rng = random.Random(4)
    pts = [(round(rng.uniform(0.3, 9.7), 1), round(rng.uniform(0.3, 9.7), 1))
           for _ in range(15)]
    out, order = [], []

    def walk(node, box, level):
        if node is None:
            return
        p, axis, left, right = node
        (x0, y0), (x1, y1) = box
        order.append(p)
        if axis == 0:
            out.append(f"\\draw[split{level % 2}] ({p[0]}, {y0}) -- ({p[0]}, {y1});")
            walk(left, ((x0, y0), (p[0], y1)), level + 1)
            walk(right, ((p[0], y0), (x1, y1)), level + 1)
        else:
            out.append(f"\\draw[split{level % 2}] ({x0}, {p[1]}) -- ({x1}, {p[1]});")
            walk(left, ((x0, y0), (x1, p[1])), level + 1)
            walk(right, ((x0, p[1]), (x1, y1)), level + 1)

    walk(build(pts), ((0, 0), (10, 10)), 0)
    out += [f"\\fill ({x}, {y}) circle (3.2pt);" for x, y in pts]
    out.append(f"\\node[root] at ({order[0][0]}, {order[0][1]}) {{}};")
    (HERE / "kd_partition.tex").write_text(HEAD + "\n".join(out) + "\n")
    return pts


def kmeans_panels():
    """Three panels of Lloyd's algorithm from seed 3: the start, one step, the end."""
    pts = blobs()
    centres = random.Random(3).sample(pts, 5)
    states = [(centres, assign(pts, centres))]
    a = states[0][1]
    c1 = [centroid([p for p, j in zip(pts, a) if j == i]) for i in range(5)]
    states.append((c1, assign(pts, c1)))
    final, fa, _ = lloyd(pts, centres)
    states.append((final, fa))
    for k, (cs, a) in enumerate(states):
        lines = [f"\\node[pt{j}] at ({x / 2:.3f}, {y / 2:.3f}) {{}};"
                 for (x, y), j in zip(pts, a)]
        lines += [f"\\node[centre] at ({x / 2:.3f}, {y / 2:.3f}) {{}};" for x, y in cs]
        (HERE / f"kmeans_{k}.tex").write_text(HEAD + "\n".join(lines) + "\n")
    return states


def dendrogram():
    """The single-linkage dendrogram: leaves in the order of the merges' tree."""
    merges = hac(PTS, min)
    root = merges[-1][0] + merges[-1][1]
    children = {tuple(sorted(a + b)): (a, b, h) for a, b, h in merges}

    def leaves(c):
        if len(c) == 1:
            return list(c)
        a, b, _ = children[tuple(sorted(c))]
        return leaves(a) + leaves(b)

    xs = {i: k for k, i in enumerate(leaves(root))}
    out = [f"\\node[leaf] at ({xs[i]}, 0) {{{NAMES[i]}}};" for i in xs]

    def draw(c):
        """The x of c's link and its height."""
        if len(c) == 1:
            return xs[c[0]], 0
        a, b, h = children[tuple(sorted(c))]
        (xa, ha), (xb, hb) = draw(a), draw(b)
        out.append(f"\\draw ({xa}, {ha:.2f}) |- ({xb}, {h:.2f}) -- ({xb}, {hb:.2f});")
        return (xa + xb) / 2, h

    draw(tuple(sorted(root)))
    (HERE / "dendrogram.tex").write_text(HEAD + "\n".join(out) + "\n")
    return merges


def depth_chart():
    """overfit.dat from the captured output of overfit.py."""
    lines = (HERE.parent / "outputs" / "overfit.txt").read_text().splitlines()[2:]
    rows = [line.split() for line in lines]
    (HERE / "overfit.dat").write_text(
        "depth leaves train test\n" + "".join(" ".join(r) + "\n" for r in rows))
    return rows


if __name__ == "__main__":
    kd_partition()
    kmeans_panels()
    dendrogram()
    depth_chart()
