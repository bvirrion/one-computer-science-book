import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_unittest_suite_passes():
    import unittest
    pt = load("listings", "planner_tests")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(pt.PlannerTests)
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    assert result.wasSuccessful() and result.testsRun == 6


def test_all_pairs_agree_with_bellman_ford():
    gr = load("listings", "graph")
    pl = load("listings", "planner")
    planner = pl.RoutePlanner()
    g = gr.from_database(planner.conn)
    for s in g.arcs:
        best = {s: 0}
        for _ in range(len(g.arcs)):
            for u in list(best):
                for v, c in g.successors(u):
                    if v not in best or best[u] + c < best[v]:
                        best[v] = best[u] + c
        assert pl.dijkstra(g, s)[0] == best


def test_exercises():
    ex = load("exercises", "rp_ex")
    pl = load("listings", "planner")
    p = pl.RoutePlanner()
    assert p.route("Bakery Corner", "South School") == (
        ["Bakery Corner", "Theatre", "South School"], 186)
    assert ex.travel_seconds(1830, 30) == 220
    assert p.conn.execute("SELECT COUNT(*), MAX(length_m) FROM road"
                          " WHERE speed_kmh = 30").fetchone() == (20, 1830)
    assert ex.place_id(p.conn, "Library") == 3
    try:
        ex.place_id(p.conn, "Libary")
        raise AssertionError
    except ValueError:
        pass
    g = ex.graph_both_ways(p.conn)
    assert g.arc_count() == 106 and ex.dijkstra(g, 3)[0][1] == 98
    d, par = ex.dijkstra(ex.graph_by_roads(p.conn), p.place_id("Old Mill"))
    assert d[p.place_id("Post Office")] == 7
    fewest = [p.names[x] for x in ex.rebuild(par, p.place_id("Post Office"))]  # the algorithm's own
    assert fewest == ["Old Mill", "South School", "Bakery Corner", "Market Hall", "Hill Park",
                      "Town Hall", "Sports Hall", "Post Office"]
    assert (p.cost_of(fewest), p.cost_of(fewest, "distance")) == (985, 9650)
    slowest = p.route("Old Mill", "Post Office")[0]
    assert (p.cost_of(slowest), p.cost_of(slowest, "distance")) == (675, 9130)
    path, seconds = p.route("Station", "Library")
    on_route = ex.roads_on_route(p.conn, [p.place_id(n) for n in path])
    assert on_route == [6, 30, 2, 1]
    for road in range(1, 54):
        if road not in on_route:
            p.close_road(road)
            assert p.route("Station", "Library")[1] == seconds
            p.reopen_road(road)
    assert ex.route_avoiding(p, "Station", "Library", "North Bridge")[1] == 572
    assert p.route("Library", "Town Square") == (
        ["Library", "Garden Centre", "Town Square"], 204)
    assert ex.within(p, "Station", 120) == ["Hill Park", "Market Hall", "North Bridge",
                                            "River Park", "Town Hall"]
