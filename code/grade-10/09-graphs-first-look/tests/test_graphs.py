import heapq
import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))
sys.path.insert(0, str(HERE.parent / "lib"))
sys.path.insert(0, str(HERE / "exercises"))
ROOT = HERE.parents[2]


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


lf = load("listings", "load_friends")
lr = load("listings", "load_roads")
friends = lf.load_friends(HERE / "listings" / "friendships.csv")
roads = lr.load_roads(HERE / "listings" / "roads.csv")


def shortest(g, a, b):
    """A reference shortest-path length (grade 12's algorithm), to check the text."""
    best, heap = {a: 0}, [(0, a)]
    while heap:
        d, v = heapq.heappop(heap)
        if v == b:
            return d
        for w, length in g[v].items():
            if d + length < best.get(w, 10**9):
                best[w] = d + length
                heapq.heappush(heap, (d + length, w))
    return None


def test_copies_match_town_tables():
    for name in ("friendships", "roads", "places"):
        assert (HERE / "listings" / f"{name}.csv").read_bytes() == (
            ROOT / "data" / "town" / f"{name}.csv").read_bytes()


def test_handshake_and_symmetry():
    t = load("exercises", "graph_tools")
    assert sum(len(n) for n in friends.values()) == 2 * len(t.edges_from_dict(friends))
    g = {}
    t.add_friendship_buggy(g, 1, 2)
    assert 1 not in g.get(2, set())
    t.add_friendship(g, 3, 4)
    assert 3 in g[4] and 4 in g[3]


def test_is_path_and_triangles():
    t = load("exercises", "graph_tools")
    assert t.is_path(friends, [3, 2, 10, 1, 28])
    assert not t.is_path(friends, [3, 1]) and not t.is_path(friends, [])
    tri = {1: {2, 3}, 2: {1, 3}, 3: {1, 2, 4}, 4: {3}}
    assert t.triangles(tri) == 1
    assert t.triangles(friends) == 2


def test_road_map_by_hand():
    small = {v: {w: d for w, d in roads[v].items() if w in {1, 3, 16, 21, 23, 24, 26}}
             for v in (1, 3, 16, 21, 23, 24, 26)}
    assert shortest(small, 3, 23) == 3840
    assert shortest(small, 23, 3) == 2570
    assert shortest(roads, 3, 23) == 3840


def test_seven_vertex_eccentricities():
    from given_graphs import distances
    edges = ["AB", "BC", "CD", "DE", "CF", "FG"]
    g = {v: set() for v in "ABCDEFG"}
    for a, b in edges:
        g[a].add(b)
        g[b].add(a)
    ecc = {v: max(distances(g, v).values()) for v in g}
    assert ecc == {"A": 4, "B": 3, "C": 2, "D": 3, "E": 4, "F": 3, "G": 4}


def test_problem_result():
    h = load("exercises", "handshakes")
    g = lf.load_friends(h.PATH)
    assert h.summary(g) == (29, 4, 7, [1, 28])
    g[1].discard(28)
    g[28].discard(1)
    assert h.summary(g) == (29, 5, 9, [5, 37])


def test_nmea():
    n = load("exercises", "nmea")
    s = "$GPGGA,093015.00,4807.0381,N,00131.5240,W,1,08,0.9,62.4,M,47.2,M,,*41"
    assert n.checksum(s) == "41"
    lat, lon = n.position(s)
    assert abs(lat - 48.1173017) < 1e-6 and abs(lon + 1.5254) < 1e-6


def test_layout_file():
    fig = load("figures", "friends_layout")
    fig.main()
    text = fig.OUT.read_text()
    assert text.count("\\draw") == 50 and text.count("\\node") == 40
