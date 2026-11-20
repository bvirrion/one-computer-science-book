"""exec.py -- relations stored as pages of tuples, and query operators in the iterator
model: each operator is a generator that pulls tuples from its children. Every page
read or written goes through a Disk, which counts it."""


class Disk:
    def __init__(self):
        self.reads = self.writes = 0

    def io(self):
        return self.reads + self.writes


class Relation:
    """Tuples (dicts) packed `per_page` to a page."""

    def __init__(self, rows, per_page=10):
        rows = list(rows)
        self.per_page = per_page
        self.pages = [rows[i : i + per_page] for i in range(0, len(rows), per_page)]

    def __len__(self):  # number of pages
        return len(self.pages)

    def rows(self):  # all tuples, without counting: for checks only
        return [t for page in self.pages for t in page]


def scan(rel, disk):
    for page in rel.pages:
        disk.reads += 1
        yield from page


def select(pred, child):
    return (t for t in child if pred(t))


def project(cols, child):
    return ({c: t[c] for c in cols} for t in child)


def materialise(child, disk, per_page=10):
    """Write a stream out as a relation: one page write per page."""
    rel = Relation(child, per_page)
    disk.writes += len(rel)
    return rel


def merge(a, b):
    """The tuple of a join: both tuples' columns (b's win on a clash)."""
    return {**a, **b}
