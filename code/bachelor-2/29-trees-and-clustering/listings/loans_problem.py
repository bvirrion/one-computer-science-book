"""loans_problem.py: which loans come back late? A tree learned from 1,000 loans with
10 % noisy labels, its depth chosen on held-out data; then the members clustered."""
import random

from dataset import loans, members, rule
from id3 import accuracy, id3, show
from kmeans import lloyd

# Part I: the data, shuffled once and split 50 / 20 / 30.
data = loans(1000, seed=11, noise=0.10)
random.Random(0).shuffle(data)
train, valid, test = data[:500], data[500:700], data[700:]
for name, part in [("training", train), ("validation", valid), ("test", test)]:
    late = sum(y for _, y in part)
    print(f"{name:10} {len(part)} loans, {late} late ({late / len(part):.1%})")

# Parts II-III: the depth that does best on validation; then one look at the test set.
scores = {d: accuracy(id3(train, d), valid) for d in range(9)}
best = max(scores, key=lambda d: (scores[d], -d))  # the shallowest among the best
print("validation accuracy, depth 0 to 8:",
      " ".join(f"{a:.3f}" for a in scores.values()))
tree = id3(train + valid, best)
show(tree)
majority = max(sum(y for _, y in test), sum(1 - y for _, y in test)) / len(test)
print(f"depth {best}: test accuracy {accuracy(tree, test):.3f}, majority baseline"
      f" {majority:.3f}, agreement with the planted rule"
      f" {accuracy(tree, [(x, rule(x)) for x, _ in test]):.3f}")

# Part IV: the 60 members by loans a year and mean days kept.
pts = members()
for k in range(1, 7):
    runs = [lloyd(pts, random.Random(s).sample(pts, k)) for s in range(10)]
    centres, a, costs = min(runs, key=lambda r: r[2][-1])
    line = f"k = {k}: cost {costs[-1]:7.1f}"
    if k == 3:
        where = ", ".join(f"({x:.1f}, {y:.1f})" for x, y in sorted(centres))
        line += f"; centres {where}"
    print(line)
