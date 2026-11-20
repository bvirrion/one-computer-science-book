"""verify_bsearch.py -- the index arithmetic of binary search on 8-bit machine integers.
The array test is left as unknown(): the proof covers every possible array. Each
verification condition is bit-blasted and handed to the CDCL solver of chapter 18."""

from bitblast import check
from vcgen import vcgen
from whilelang import parse, run

SEARCH = """
lo = 0
hi = n
while lo < hi:
    invariant(INV)
    variant(hi - lo)
    mid = MID
    assert lo <= mid and mid < hi
    if unknown():
        lo = mid + 1
    else:
        hi = mid
"""


def report(title, mid, inv="lo <= hi and hi <= n"):
    print(title)
    source = SEARCH.replace("MID", mid).replace("INV", inv)
    for name, vc in vcgen("True", source, "lo == hi and hi <= n"):
        valid, cex, (variables, clauses) = check(vc)
        verdict = "valid" if valid else f"FAILS, e.g. {cex}"
        print(f"  {name:<9} {variables:>5} variables {clauses:>6} clauses  {verdict}")
    return source


if __name__ == "__main__":
    wrong = report("midpoint (lo + hi) // 2:", "(lo + hi) // 2")
    try:
        run(parse(wrong), {"n": 255}, choose=lambda: True)
    except AssertionError as failure:
        print(
            f"  run with n = 255, always going right, the assert fails:\n    {failure}"
        )
    report("midpoint lo + (hi - lo) // 2:", "lo + (hi - lo) // 2")
    report(
        "invariant lo < hi (wrong):", "lo + (hi - lo) // 2", inv="lo < hi and hi <= n"
    )
