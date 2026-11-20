"""ex5_hash.py -- a hash join that always builds its table on R, the first input.
Its results are right; count its page I/O against a join that builds on the smaller
input when R is the larger one, and fix it."""

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from exec import merge, scan  # noqa: E402
from joins import partition  # noqa: E402


def join_building_on(build, probe, kb, kp, B, disk, build_is_left=True):
    """One pass if the build input fits in B - 2 pages, else partition both first."""
    pairs = [(build, probe)]
    if len(build) > B - 2:
        pairs = list(zip(partition(build, kb, B, disk), partition(probe, kp, B, disk)))
    out = []
    for bp, pp in pairs:
        table = defaultdict(list)
        for x in scan(bp, disk):
            table[x[kb]].append(x)
        for y in scan(pp, disk):
            out += [
                merge(x, y) if build_is_left else merge(y, x)
                for x in table.get(y[kp], ())
            ]
    return out


def buggy_hash_join(R, S, a, b, B, disk):
    return join_building_on(R, S, a, b, B, disk)


def fixed_hash_join(R, S, a, b, B, disk):
    if len(S) < len(R):
        return join_building_on(S, R, b, a, B, disk, build_is_left=False)
    return join_building_on(R, S, a, b, B, disk)
