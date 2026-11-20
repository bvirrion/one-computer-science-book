"""exo_block_size.py: misses of a tiled transpose, by tile size (exercise 11)."""
from cache import Cache

N = 128                        # 128 x 128 ints: two 64 KiB matrices, a 4 KiB cache
A, B = 0, 4 * N * N


def misses(t):
    c = Cache(size=4096, line=64, ways=4)
    for ii in range(0, N, t):
        for jj in range(0, N, t):
            for i in range(ii, ii + t):
                for j in range(jj, jj + t):
                    c.access(A + 4 * (i * N + j))
                    c.access(B + 4 * (j * N + i), write=True)
    return c.misses


print(f"{'tile':>5}{'misses':>8}{'per element':>13}")
for t in [1, 2, 4, 8, 16, 32, 64, 128]:
    m = misses(t)
    print(f"{t:>5}{m:>8}{m / N ** 2:>13.3f}")
