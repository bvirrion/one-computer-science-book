import csv

from dijkstra import dijkstra

with open("places.csv", newline="") as f:
    NAMES = {int(r["place_id"]): r["name"] for r in csv.DictReader(f)}
g = {p: {} for p in NAMES}
with open("roads.csv", newline="") as f:
    for r in csv.DictReader(f):
        a, b, metres = int(r["from_place"]), int(r["to_place"]), int(r["length_m"])
        g[a][b] = metres
        if r["one_way"] == "0":
            g[b][a] = metres

dist, parent = dijkstra(g, 2)                        # from the Station
far = sorted(dist, key=dist.get)
print("reached:", len(dist), "places | farthest:", NAMES[far[-1]], dist[far[-1]], "m")
for p in [1, 3, 4]:
    print(f"  Station -> {NAMES[p]:13} {dist[p]:>5} m")
there, back = dijkstra(g, 1)[0][3], dijkstra(g, 3)[0][1]
print(f"Town Square -> Library {there} m, Library -> Town Square {back} m")
