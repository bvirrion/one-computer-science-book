"""blur_sim.py: the cache misses of a 3 x 3 box blur, in three traversal orders."""
from cache import Cache

N = 256                       # 256 x 256 pixels of 4 bytes: 256 KiB; the cache: 4 KiB
IN = 0                        # the address of the input image


def pixels(order, strip=16):
    """The (y, x) of the output pixels, interior only, in the given order."""
    inner = range(1, N - 1)
    if order == "rows":
        return [(y, x) for y in inner for x in inner]
    if order == "columns":
        return [(y, x) for x in inner for y in inner]
    return [(y, x) for x0 in range(0, N, strip) for y in inner     # strips of columns
            for x in range(max(x0, 1), min(x0 + strip, N - 1))]


def read_misses(order, strip=16):
    """Misses of the reads of the input image; the output is written once per pixel."""
    c = Cache(size=4096, line=64, ways=4)
    for y, x in pixels(order, strip):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                c.access(IN + 4 * ((y + dy) * N + x + dx))
    return c.hits + c.misses, c.misses


if __name__ == "__main__":
    print(f"{'order':<18}{'reads':>8}{'misses':>8}{'per pixel':>11}")
    for order, strip in [("rows", 0), ("columns", 0), ("strips", 16), ("strips", 64)]:
        reads, m = read_misses(order, strip)
        name = f"{order} of {strip}" if strip else order
        print(f"{name:<18}{reads:>8}{m:>8}{m / (N - 2) ** 2:>11.4f}")
