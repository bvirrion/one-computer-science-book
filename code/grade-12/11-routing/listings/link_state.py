"""Link-state routing: every router learns the whole map, then runs Dijkstra."""
from network import by_rate, graph


def flood(g):
    """Each router's list of links reaches every router; count the messages sent."""
    known = {r: {r} for r in g}                  # whose link lists r has received
    messages = 0
    for origin in g:
        queue = [(origin, None)]                 # (router that forwards, received from)
        while queue:
            r, came_from = queue.pop()
            for n in g[r]:
                if n == came_from:
                    continue                     # never sent back where it came from
                messages += 1
                if origin not in known[n]:
                    known[n].add(origin)         # new: keep it and pass it on
                    queue.append((n, r))
    return known, messages


def table(g, source):
    """Dijkstra from source; for each destination: (cost, first router on the way)."""
    tentative, best = {source: (0, source)}, {}
    while tentative:
        v = min(tentative, key=lambda r: (tentative[r], r))     # smallest cost
        d, first = best[v] = tentative.pop(v)                   # v is finished
        for w, cost in g[v].items():
            if w not in best and (w not in tentative or d + cost < tentative[w][0]):
                tentative[w] = (d + cost, w if v == source else first)
    return best


if __name__ == "__main__":
    g = graph(by_rate)
    known, messages = flood(g)
    print("every router knows all", len(g), "lists:", all(len(k) == len(g)
                                                         for k in known.values()))
    print("messages sent while flooding:", messages)
    for r in "AE":
        t = table(g, r)
        print(f"{r}'s table: " + "  ".join(f"{d}: {c} {n}" for d, (c, n) in
                                           sorted(t.items()) if d != r))
