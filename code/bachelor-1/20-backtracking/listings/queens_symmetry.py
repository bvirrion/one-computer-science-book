"""queens_symmetry.py: the 92 solutions of eight queens, grouped by the eight symmetries
of the square (rotations and reflections)."""

from itertools import permutations


def solutions(n):
    """Brute force over the n! placements with one queen per row and per column."""
    return [p for p in permutations(range(n))
            if len({r - c for r, c in enumerate(p)}) == n
            and len({r + c for r, c in enumerate(p)}) == n]


def transforms(p):
    """The images of the solution p (cols[r] = p[r]) under the eight symmetries."""
    n = len(p)
    cells = {(r, c) for r, c in enumerate(p)}
    maps = [lambda r, c: (r, c), lambda r, c: (c, n - 1 - r),           # identity, 90
            lambda r, c: (n - 1 - r, n - 1 - c), lambda r, c: (n - 1 - c, r),  # 180 270
            lambda r, c: (r, n - 1 - c), lambda r, c: (n - 1 - r, c),    # mirrors
            lambda r, c: (c, r), lambda r, c: (n - 1 - c, n - 1 - r)]    # diagonals
    images = []
    for m in maps:
        moved = sorted(m(r, c) for r, c in cells)
        images.append(tuple(c for _, c in moved))
    return images


def main():
    sols = solutions(8)
    seen, orbits = set(), []
    for p in sols:
        if p in seen:
            continue
        orbit = set(transforms(p))
        seen |= orbit
        orbits.append((min(orbit), len(orbit)))
    print(len(sols), "solutions,", len(orbits), "up to symmetry")
    sizes = sorted(size for _, size in orbits)
    print("orbit sizes:", sizes)
    for rep, size in orbits:
        if size < 8:
            print("the symmetric one:", rep, "unchanged by the half-turn:",
                  transforms(rep)[2] == rep)


if __name__ == "__main__":
    main()
