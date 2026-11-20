"""Milestone 5: the planner's tests, run with unittest."""
import random
import unittest

from graph import Graph, from_database, travel_seconds
from planner import RoutePlanner, dijkstra


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.planner = RoutePlanner()

    def test_travel_time(self):
        self.assertEqual(travel_seconds(1000, 36), 100)    # 36 km/h is 10 m/s
        self.assertEqual(travel_seconds(1210, 50), 87)

    def test_one_way_road(self):
        g = from_database(self.planner.conn)
        self.assertEqual(g.arc_count(), 105)
        self.assertEqual(g.one_way_arcs(), [(1, 3)])

    def test_unknown_place(self):
        with self.assertRaises(ValueError):
            self.planner.route("Station", "Libary")

    def test_cost_is_sum(self):
        path, seconds = self.planner.route("Old Mill", "Post Office")
        self.assertEqual(self.planner.cost_of(path), seconds)

    def test_dijkstra_vs_slow_method(self):
        rng = random.Random(4)
        for _ in range(100):
            g, n = Graph(), rng.randint(2, 7)
            for u in range(n):
                g.add_vertex(u)
                for v in rng.sample(range(n), rng.randint(0, n - 1)):
                    if v != u:
                        g.add_arc(u, v, rng.randint(1, 9))
            best = {0: 0}                        # slow but sure: n rounds
            for _ in range(n):
                for u in list(best):
                    for v, c in g.successors(u):
                        if v not in best or best[u] + c < best[v]:
                            best[v] = best[u] + c
            self.assertEqual(dijkstra(g, 0)[0], best)

    def test_closing_never_helps(self):
        before = self.planner.route("Station", "Library")[1]
        for road in range(1, 54):
            self.planner.close_road(road)
            try:
                after = self.planner.route("Station", "Library")[1]
                self.assertGreaterEqual(after, before)
            except ValueError:
                pass                             # the town split: no route at all
            self.planner.reopen_road(road)


if __name__ == "__main__":
    unittest.main(verbosity=2)
