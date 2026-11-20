"""workspan.py -- work and span of the chapter's algorithms, measured on their
computation DAGs: one node per unit-time operation, an edge from each operation
to the operations that use its result. Work = nodes, span = nodes on a longest path."""

from functools import cache


def work_span(preds):
    """preds: node -> the nodes it depends on (a DAG)."""

    @cache
    def depth(v):
        return 1 + max((depth(u) for u in preds[v]), default=0)

    return len(preds), max(depth(v) for v in preds)


def reduction(n):
    """Pairwise sums of n = 2^k inputs: a tree of n - 1 additions."""
    preds, level = {}, [None] * n  # the inputs are given, not computed
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            v = ("add", len(level), i)
            preds[v] = [u for u in level[i : i + 2] if u is not None]
            nxt.append(v)
        level = nxt
    return preds


def blelloch(n):
    """The additions of the up-sweep and down-sweep, as in scan.rs."""
    preds, last = {}, [None] * n  # last[i]: the operation that last wrote x[i]
    d = 1
    while d < n:
        for i in range(2 * d - 1, n, 2 * d):
            v = ("up", d, i)
            preds[v] = [u for u in (last[i], last[i - d]) if u is not None]
            last[i] = v
        d *= 2
    last[n - 1] = None  # the root is set to 0
    while d > 1:
        d //= 2
        for i in range(2 * d - 1, n, 2 * d):
            v = ("down", d, i)
            preds[v] = [u for u in (last[i], last[i - d]) if u is not None]
            last[i - d] = last[i] = v  # the swap moves a value, the add makes one
    return preds


def hillis_steele(n):
    preds, last, d = {}, [None] * n, 1
    while d < n:
        new = list(last)
        for j in range(d, n):
            new[j] = ("hs", d, j)
            preds[new[j]] = [u for u in (last[j], last[j - d]) if u is not None]
        last, d = new, 2 * d
    return preds


def merge_sort(n, lo=0):
    """Fork-join merge sort with a sequential merge: a chain of n steps per merge."""
    if n == 1:
        return {}, None
    (left, a), (right, b) = merge_sort(n // 2, lo), merge_sort(n // 2, lo + n // 2)
    preds = left | right
    prev = [u for u in (a, b) if u is not None]
    for k in range(n):
        v = ("merge", lo, n, k)
        preds[v], prev = prev, [v]
    return preds, prev[0]


if __name__ == "__main__":
    print(f"{'algorithm':<26} {'n':>5} {'work':>7} {'span':>5} {'parallelism':>12}")
    for name, build in (
        ("sum (reduction)", reduction),
        ("Hillis-Steele scan", hillis_steele),
        ("Blelloch scan", blelloch),
        ("merge sort, serial merge", lambda n: merge_sort(n)[0]),
    ):
        for n in (8, 1024):
            w, s = work_span(build(n))
            print(f"{name:<26} {n:>5} {w:>7} {s:>5} {w / s:>12.1f}")
