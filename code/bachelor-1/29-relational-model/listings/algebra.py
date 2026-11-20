"""algebra.py: relational algebra on sets. A relation is a schema (a tuple of attribute
names) and a set of tuples; every operator returns a new relation."""

from collections import defaultdict


class Relation:
    def __init__(self, schema, rows):
        self.schema = tuple(schema)
        self.rows = frozenset(tuple(r) for r in rows)  # a set: no duplicates, no order

    def dicts(self):
        return [dict(zip(self.schema, r)) for r in self.rows]

    def __eq__(self, other):
        return set(self.schema) == set(other.schema) and self.rows == project(
            other, self.schema).rows

    def __len__(self):
        return len(self.rows)


def select(r, condition):  # sigma: the tuples that satisfy the condition
    return Relation(r.schema, [t for t, d in zip(r.rows, r.dicts()) if condition(d)])


def project(r, attrs):  # pi: keep some attributes; duplicates merge
    idx = [r.schema.index(a) for a in attrs]
    return Relation(attrs, [tuple(t[i] for i in idx) for t in r.rows])


def rename(r, mapping):  # rho: new names for some attributes
    return Relation([mapping.get(a, a) for a in r.schema], r.rows)


def union(r, s):
    assert set(r.schema) == set(s.schema), "union needs the same attributes"
    return Relation(r.schema, r.rows | project(s, r.schema).rows)


def difference(r, s):
    assert set(r.schema) == set(s.schema), "difference needs the same attributes"
    return Relation(r.schema, r.rows - project(s, r.schema).rows)


def product(r, s):
    assert not set(r.schema) & set(s.schema), "rename the common attributes first"
    return Relation(r.schema + s.schema, [t + u for t in r.rows for u in s.rows])


def natural_join(r, s):
    """Pairs of tuples that agree on the common attributes, each attribute kept once."""
    common = [a for a in r.schema if a in s.schema]
    rest = [a for a in s.schema if a not in common]
    by_key = defaultdict(list)  # the tuples of s, grouped by their common values
    for d in s.dicts():
        by_key[tuple(d[a] for a in common)].append(tuple(d[a] for a in rest))
    rows = [t + u for t, d in zip(r.rows, r.dicts())
            for u in by_key[tuple(d[a] for a in common)]]
    return Relation(r.schema + tuple(rest), rows)


def theta_join(r, s, condition):
    return select(product(r, s), condition)


def intersection(r, s):  # derived: R - (R - S)
    return difference(r, difference(r, s))


def division(r, s):
    """The x such that (x, y) is in r for every y in s; derived from pi, x and -."""
    xs = [a for a in r.schema if a not in s.schema]
    candidates = project(r, xs)
    missing = difference(natural_join(candidates, s), r)  # pairs that should be there
    return difference(candidates, project(missing, xs))


def group(r, keys, name, function, attr):
    """gamma: one tuple per value of the keys, with function applied to attr."""
    groups = defaultdict(list)
    for d in r.dicts():
        groups[tuple(d[k] for k in keys)].append(d[attr])
    rows = [k + (function(v),) for k, v in groups.items()]
    return Relation(tuple(keys) + (name,), rows)


def table(name):
    """A table of the town as a relation (NULL becomes None)."""
    import town
    rows = town.load(name)
    return Relation(list(rows[0]), [tuple(d.values()) for d in rows])
