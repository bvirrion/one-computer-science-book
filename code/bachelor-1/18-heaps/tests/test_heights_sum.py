"""The heap identity: the heights of a heap of n nodes add up to n - v(n)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))

from heights_sum import heights, nu, sums_of_heights  # noqa: E402


def test_incremental_matches_direct():
    sums = sums_of_heights(600)
    assert all(sums[n] == sum(heights(n)) for n in range(601))


def test_identity():
    sums = sums_of_heights(10000)
    assert all(sums[n] == n - nu(n) for n in range(10001))
