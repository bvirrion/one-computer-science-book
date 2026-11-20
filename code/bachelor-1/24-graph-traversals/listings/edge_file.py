"""edge_file.py: a graph written to a text file as an edge list, and read back."""

import tempfile
from pathlib import Path

from graph import Graph, roads


def write(g, path):
    """First line: 'directed' or 'undirected', and the vertices; one edge a line."""
    lines = [("directed" if g.directed else "undirected") + " "
             + " ".join(map(str, g.vertices()))]
    lines += [f"{u} {v}" for u, v in g.edges()]
    Path(path).write_text("\n".join(lines) + "\n")


def read(path):
    first, *rest = Path(path).read_text().splitlines()
    kind, *names = first.split()
    g = Graph(directed=kind == "directed")
    for v in names:
        g.add_vertex(int(v))
    for line in rest:
        u, v = map(int, line.split())
        g.add_edge(u, v)
    return g


def main():
    g = roads()
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "roads.txt"
        write(g, path)
        text = path.read_text().splitlines()
        h = read(path)
    print(f"{len(text)} lines; first two edges: {text[1]!r}, {text[2]!r}")
    same = {v: sorted(h.adj[v]) for v in h.adj} == {v: sorted(g.adj[v]) for v in g.adj}
    print("read back: same vertices and arcs:", same)


if __name__ == "__main__":
    main()
