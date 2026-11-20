"""three_c_demo.py: the misses of the column-order sum and of a cyclic sweep."""
from three_c import classify
from trace_demo import load_addresses

_, column = load_addresses(1)
cyclic = [32 * (k % 33) for k in range(33 * 10)]    # 33 lines, swept 10 times
for name, trace in [("column order", column), ("cyclic sweep of 33 lines", cyclic)]:
    print(name)
    for ways, label in [(1, "direct-mapped"), (2, "2-way"), (32, "fully associative")]:
        misses, c = classify(trace, 1024, 32, ways)
        print(f"  {label:<18} {misses:>5} misses = {c['compulsory']:>4} compulsory"
              f" + {c['capacity']:>4} capacity + {c['conflict']:>4} conflict")
