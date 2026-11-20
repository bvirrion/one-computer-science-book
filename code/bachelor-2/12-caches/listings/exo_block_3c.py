"""exo_block_3c.py: the misses of the tiled transpose, classified (exercise 11)."""
from three_c import classify

N = 128
A, B = 0, 4 * N * N


def trace(t):
    out = []
    for ii in range(0, N, t):
        for jj in range(0, N, t):
            for i in range(ii, ii + t):
                for j in range(jj, jj + t):
                    out += [A + 4 * (i * N + j), B + 4 * (j * N + i)]
    return out


for t in [1, 2, 4, 8, 16]:
    misses, c = classify(trace(t), 4096, 64, 4)
    print(f"tile {t:>2}: {misses:>5} = {c['compulsory']} compulsory"
          f" + {c['capacity']:>5} capacity + {c['conflict']:>5} conflict")
