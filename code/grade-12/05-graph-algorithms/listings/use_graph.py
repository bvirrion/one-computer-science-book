from dijkstra import dijkstra
from graph_class import Graph

g = Graph()
for a, b, w in [("S", "A", 4), ("S", "B", 1), ("A", "B", 2), ("A", "C", 5),
                ("B", "D", 8), ("C", "D", 1), ("C", "T", 3), ("D", "T", 6)]:
    g.add_edge(a, b, w)
g.add_edge("T", "X", 2, directed=True)
print(len(g), "vertices | neighbours of A:", g.neighbours("A"),
      "| of X:", g.neighbours("X"))
print("Dijkstra on the class:", dijkstra(g, "S")[0])
