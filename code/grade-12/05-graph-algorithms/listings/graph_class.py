"""A graph as a class: the dictionary of dictionaries hidden behind methods."""


class Graph:
    def __init__(self):
        self._adj = {}

    def add_vertex(self, v):
        self._adj.setdefault(v, {})

    def add_edge(self, a, b, weight=1, directed=False):
        self.add_vertex(a)
        self.add_vertex(b)
        self._adj[a][b] = weight
        if not directed:
            self._adj[b][a] = weight

    def neighbours(self, v):
        return list(self._adj[v])

    def __iter__(self):                  # for v in graph: the vertices
        return iter(self._adj)

    def __getitem__(self, v):            # graph[v]: neighbour -> weight
        return dict(self._adj[v])

    def __len__(self):
        return len(self._adj)
