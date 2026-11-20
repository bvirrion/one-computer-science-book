from load_friends import load_friends

g = load_friends("friendships.csv")
degree = {p: len(g[p]) for p in g}
count = {}
for d in degree.values():
    count[d] = count.get(d, 0) + 1
for d in sorted(count):
    print(f"degree {d}: {count[d]:2} people  " + "#" * count[d])
print("sum of degrees:", sum(degree.values()))
print("most friends:", [p for p in g if degree[p] == max(degree.values())])
