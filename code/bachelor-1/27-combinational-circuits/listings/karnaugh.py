"""karnaugh.py: a Karnaugh map of four variables, and the prime implicants of a function
found by merging terms that differ in one variable (Quine--McCluskey)."""

GRAY = ["00", "01", "11", "10"]  # neighbours differ in one bit, and so do the ends


def kmap(ones, dont_care=()):
    """Rows: ab in Gray order; columns: cd in Gray order."""
    lines = ["ab\\cd " + "  ".join(GRAY)]
    for ab in GRAY:
        cells = []
        for cd in GRAY:
            m = int(ab + cd, 2)
            cells.append(" 1" if m in ones else " -" if m in dont_care else " .")
        lines.append(f"  {ab}  " + "  ".join(cells))
    return "\n".join(lines)


def merge(s, t):
    """Two terms such as '0-11' and '1-11' that differ in one position give '--11'."""
    diff = [i for i in range(len(s)) if s[i] != t[i]]
    if len(diff) == 1 and "-" not in (s[diff[0]], t[diff[0]]):
        return s[:diff[0]] + "-" + s[diff[0] + 1:]
    return None


def prime_implicants(ones, dont_care=(), n=4):
    terms = {format(m, f"0{n}b") for m in set(ones) | set(dont_care)}
    primes = set()
    while terms:
        merged, used = set(), set()
        for s in terms:
            for t in terms:
                m = merge(s, t)
                if m:
                    merged.add(m)
                    used |= {s, t}
        primes |= terms - used  # a term that merges with nothing is prime
        terms = merged
    return sorted(primes)


def covers(term, m, n=4):
    return all(c in "-" + b for c, b in zip(term, format(m, f"0{n}b")))


def essential(primes, ones):
    """The primes that alone cover some 1 of the function."""
    return sorted({ps[0] for m in ones
                   if len(ps := [p for p in primes if covers(p, m)]) == 1})


def as_product(term, names="abcd"):
    return "".join(n + ("'" if c == "0" else "")
                   for n, c in zip(names, term) if c != "-")


if __name__ == "__main__":
    ones = [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]
    print(kmap(ones))
    primes = prime_implicants(ones)
    print("prime implicants:", ", ".join(as_product(p) for p in primes))
    print("essential:", ", ".join(as_product(p) for p in essential(primes, ones)))
