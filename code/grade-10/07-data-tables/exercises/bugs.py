"""Exercises 5, 7 and 11: three bugs and their fixes."""


def sort_years_buggy(rows):
    return sorted(rows, key=lambda r: r["year"])  # years read as text


def sort_years(rows):
    return sorted(rows, key=lambda r: int(r["year"]))


def duplicates_buggy(lines):
    seen, dup = set(), []
    for line in lines:
        if line in seen:
            dup.append(line)
        seen.add(line)
    return dup


def duplicates(lines):
    seen, dup = set(), []
    for line in lines:
        key = tuple(cell.strip() for cell in line.split(","))
        if key in seen:
            dup.append(line)
        seen.add(key)
    return dup


def mean_buggy(values):
    present = [v for v in values if v is not None]
    return sum(present) / len(present)


def mean(values, error_codes=(-99.0,)):
    present = [v for v in values if v is not None and v not in error_codes]
    return sum(present) / len(present)
