"""Exercise 13: the transpose of a table, by a nested comprehension."""


def transpose(table):
    """Return the transpose of a non-empty rectangular table: row i is column i."""
    return [[row[j] for row in table] for j in range(len(table[0]))]
