"""Exercises 9 and 11: the smallest structure over all field orders, and the cost of strcat."""

from itertools import permutations


def struct_size(fields):
    """fields: (size, alignment) pairs in order; the C layout rules of this machine."""
    offset, biggest = 0, 1
    for size, align in fields:
        offset = (offset + align - 1) // align * align
        offset += size
        biggest = max(biggest, align)
    return (offset + biggest - 1) // biggest * biggest


def test_decreasing_alignment_is_minimal():
    CHAR, SHORT, INT, DOUBLE = (1, 1), (2, 2), (4, 4), (8, 8)
    cases = [
        [CHAR, DOUBLE, CHAR, INT],             # layout.c, 24 then 16
        [CHAR, INT, CHAR, SHORT],              # exo_sizes.c, 12 then 8
        [CHAR, SHORT, CHAR, DOUBLE, INT, CHAR, SHORT],
        [(10, 1), INT],                        # struct person of overflow.c
    ]
    for fields in cases:
        best = min(struct_size(list(p)) for p in permutations(fields))
        sorted_fields = sorted(fields, key=lambda f: -f[1])
        assert struct_size(sorted_fields) == best
        payload = sum(s for s, _ in fields)
        biggest = max(a for _, a in fields)
        assert best == (payload + biggest - 1) // biggest * biggest
    assert struct_size([CHAR, DOUBLE, CHAR, INT]) == 24
    assert struct_size([DOUBLE, INT, CHAR, CHAR]) == 16


def strcat_bytes(n, w):
    """Bytes read and written building n words of w letters plus a space, word by word with strcat."""
    total, length = 0, 0
    for _ in range(n):
        total += length + 1  # strcat reads the destination up to its zero byte
        total += w + 1 + 1  # then copies the word, the space and a new zero byte
        length += w + 1
    return total


def test_strcat_is_quadratic():
    for n in (1, 10, 100, 1000):
        for w in (1, 5):
            assert strcat_bytes(n, w) == (w + 1) * n * (n - 1) // 2 + n * (w + 3)
