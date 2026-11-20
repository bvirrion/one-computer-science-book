"""Every prediction measures its distance to every example: count them."""
from distance import distance
from knn import predict
from parcels import make_items, split

calls = 0


def counted(a, b):
    global calls
    calls += 1
    return distance(a, b)


train, validation, test = split(make_items())
for examples, name in [(validation, "validation"), (validation + test, "both")]:
    calls = 0
    for x in examples:
        predict(train, x, 5, dist=counted)
    print(f"{len(examples):3} predictions ({name}) with {len(train)} examples:",
          calls, "distances")
