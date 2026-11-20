"""Naive search, Horspool and str.find, timed on a million random letters."""
import random
import time

from horspool import horspool
from naive import search_naive


def all_find(text, p):
    positions, i = [], text.find(p)
    while i != -1:
        positions.append(i)
        i = text.find(p, i + 1)
    return positions


def seconds(f, *args):
    start = time.perf_counter()
    result = f(*args)
    return time.perf_counter() - start, result


rng = random.Random(3)
text = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(1_000_000))
for p in ["town", "station square"]:
    t_naive, (found, _) = seconds(search_naive, text, p)
    t_hors, (found_h, _) = seconds(horspool, text, p)
    t_find, found_f = seconds(all_find, text, p)
    assert found == found_h == found_f
    print(f"{p!r:16} found {len(found)}:  naive {t_naive:5.2f} s   Horspool"
          f" {t_hors:5.2f} s   str.find {t_find * 1000:6.2f} ms")
