"""Looking up a key among n pairs: scanning a list against a dictionary."""
import timeit



def scan(pairs, key):
    for k, v in pairs:
        if k == key:
            return v


for n in [1_000, 10_000, 100_000]:
    pairs = [(f"name{i}", i) for i in range(n)]
    book = dict(pairs)
    key = f"name{n - 1}"                       # the worst case for the scan
    env = {"scan": scan, "pairs": pairs, "book": book, "key": key}
    t_list = min(timeit.repeat("scan(pairs, key)", globals=env, number=20)) / 20
    t_dict = min(timeit.repeat("book[key]", globals=env, number=20_000)) / 20_000
    print(f"n = {n:>7}: list {t_list * 1e6:9.2f} us   dict {t_dict * 1e6:6.3f} us"
          f"   ratio {t_list / t_dict:8.0f}")
