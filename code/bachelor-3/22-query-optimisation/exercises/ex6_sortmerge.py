"""ex6_sortmerge.py -- sort-merge join when the join column has duplicates on both
sides: every tuple of a group of equal keys in R meets every tuple of the matching
group in S."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from exec import merge, scan  # noqa: E402
from sort_ext import external_sort  # noqa: E402


def groups(it, key):
    """Consecutive tuples with equal keys, as (key, list) pairs."""
    group = []
    for t in it:
        if group and key(t) != key(group[0]):
            yield key(group[0]), group
            group = []
        group.append(t)
    if group:
        yield key(group[0]), group


def sort_merge_dup(R, S, a, b, B, disk):
    Rs, _ = external_sort(R, lambda t: t[a], B, disk)
    Ss, _ = external_sort(S, lambda t: t[b], B, disk)
    out = []
    gs = groups(scan(Ss, disk), lambda t: t[b])
    s = next(gs, None)
    for k, rgroup in groups(scan(Rs, disk), lambda t: t[a]):
        while s is not None and s[0] < k:
            s = next(gs, None)
        if s is not None and s[0] == k:
            out += [merge(r, t) for r in rgroup for t in s[1]]
    for _ in gs:
        pass
    return out
