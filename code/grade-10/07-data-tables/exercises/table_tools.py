"""Exercises 3, 6, 9 and 12: projection, counting and medians per group, a left join."""


def project(table, cols):
    """Keep only the columns cols of every record, in that order."""
    return [{c: row[c] for c in cols} for row in table]


def group_count(table, col):
    """Return a dict: value of col -> number of records with that value."""
    counts = {}
    for row in table:
        counts[row[col]] = counts.get(row[col], 0) + 1
    return counts


def median(values):
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


def median_by(table, group, col):
    """Return a dict: value of group -> median of col (None skipped)."""
    groups = {}
    for row in table:
        if row[col] is not None:
            groups.setdefault(row[group], []).append(row[col])
    return {g: median(v) for g, v in groups.items()}


def left_join(left, right, key):
    """Join on key, keeping every left record; missing right columns become None."""
    index = {}
    for r in right:
        index.setdefault(r[key], []).append(r)
    right_cols = [c for c in right[0] if c != key] if right else []
    result = []
    for row in left:
        matches = index.get(row[key])
        if matches:
            result.extend({**row, **m} for m in matches)
        else:
            result.append({**row, **{c: None for c in right_cols}})
    return result
