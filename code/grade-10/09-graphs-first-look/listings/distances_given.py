from given_graphs import components, distances
from load_friends import load_friends

g = load_friends("friendships.csv")
from_1 = distances(g, 1)
for d in range(max(from_1.values()) + 1):
    print(f"at distance {d} from 1:", sorted(v for v in from_1 if from_1[v] == d))

largest = components(g)[0]
eccentricity = {v: max(distances(g, v).values()) for v in largest}
radius = min(eccentricity.values())
diameter = max(eccentricity.values())
print("radius", radius, " diameter", diameter)
print("centre:", [v for v in sorted(largest) if eccentricity[v] == radius])
print("eccentricity 7:", [v for v in sorted(largest) if eccentricity[v] == diameter])
