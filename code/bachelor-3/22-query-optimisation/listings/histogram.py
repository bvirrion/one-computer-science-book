"""histogram.py -- equi-width and equi-depth histograms of the town's daily rain,
and the row counts they predict for three conditions against the true counts;
then two correlated columns of the loans, where multiplying selectivities fails."""

import town


def equi_width(values, k):
    lo, hi = min(values), max(values)
    width = (hi - lo) / k
    buckets = [[lo + i * width, lo + (i + 1) * width, []] for i in range(k)]
    for v in values:
        buckets[min(int((v - lo) / width), k - 1)][2].append(v)
    return [(a, b, len(vs), len(set(vs))) for a, b, vs in buckets]


def equi_depth(values, k):
    """k buckets of (almost) equal counts, cut at positions in sorted order."""
    vs = sorted(values)
    cuts = [len(vs) * i // k for i in range(k + 1)]
    return [
        (vs[a], vs[b - 1], b - a, len(set(vs[a:b]))) for a, b in zip(cuts, cuts[1:])
    ]


def estimate(hist, lo, hi):
    """Rows with lo <= v <= hi, assuming values spread evenly inside each bucket;
    an equality (lo == hi) assumes each distinct value of the bucket equally often."""
    total = 0.0
    for a, b, count, distinct in hist:
        if lo == hi:
            total += count / distinct if a <= lo <= b else 0
        elif a == b:
            total += count if lo <= a <= hi else 0
        else:
            total += count * max(0.0, min(hi, b) - max(lo, a)) / (b - a)
    return total


if __name__ == "__main__":
    rain = [w["rain_mm"] for w in town.load("weather")]
    hists = {"equi-width": equi_width(rain, 8), "equi-depth": equi_depth(rain, 8)}
    print("bucket   equi-width        rows   equi-depth     rows")
    for i, (w, d) in enumerate(zip(*hists.values())):
        print(
            f"{i:>6}   [{w[0]:5.2f}, {w[1]:5.2f}]  {w[2]:>5}"
            f"   [{d[0]:4.1f}, {d[1]:4.1f}]  {d[2]:>5}"
        )
    print("condition            true   equi-width   equi-depth")
    for label, lo, hi in (
        ("rain = 0", 0, 0),
        ("1 <= rain <= 3", 1, 3),
        ("rain >= 10", 10, 99),
    ):
        true = sum(lo <= v <= hi for v in rain)
        est = [estimate(h, lo, hi) for h in hists.values()]
        print(f"{label:<18} {true:>6} {est[0]:>12.1f} {est[1]:>12.1f}")
    loans = town.load("loans")
    n = len(loans)
    s1 = sum(t["out_date"] < "2025-03-01" for t in loans) / n
    s2 = sum(t["due_date"] < "2025-03-01" for t in loans) / n
    both = sum(
        t["out_date"] < "2025-03-01" and t["due_date"] < "2025-03-01" for t in loans
    )
    print(f"loans out before March: {s1:.3f}, due before March: {s2:.3f}")
    print(f"both: independence estimates {n * s1 * s2:.1f} rows, true {both}")
