"""dijkstra_neg.py: Dijkstra's algorithm on a graph with one negative arc."""

from dijkstra import dijkstra

GRAPH = {"s": [("a", 2), ("b", 3)], "a": [("t", 1)], "b": [("a", -2)], "t": []}

if __name__ == "__main__":
    dist, _, _ = dijkstra(GRAPH, "s")
    print("Dijkstra:", dist)
    print("true:    ", {"s": 0, "a": 1, "b": 3, "t": 2})
