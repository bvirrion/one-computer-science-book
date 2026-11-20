from given_graphs import components
from load_friends import load_friends

g = load_friends("friendships.csv")
for part in components(g):
    people = [str(p) for p in sorted(part)]
    shown = people if len(people) <= 12 else people[:12] + ["..."]
    print(len(part), "people:", ", ".join(shown))
