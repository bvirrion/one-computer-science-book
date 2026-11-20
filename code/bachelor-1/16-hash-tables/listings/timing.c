// timing.c: nanoseconds per successful search as the load factor grows, m = 2^16,
// best of three runs.
// capture: with=chain.c,probe.c,hashes.c
#define _POSIX_C_SOURCE 199309L
#include "chain.h"
#include "probe.h"
#include <stdio.h>
#include <time.h>

enum { M = 1 << 16 };
static char keys[M][12];

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

int main(void) {
    for (int i = 0; i < M; i++) snprintf(keys[i], sizeof keys[i], "key%d", i);
    printf("%5s %10s %10s   (ns per search)\n", "alpha", "chaining", "probing");
    const double alphas[] = {0.25, 0.5, 0.75, 0.9, 0.95};
    for (int a = 0; a < 5; a++) {
        int n = (int)(alphas[a] * M), v;
        chain *c = chain_new(M, hash_fnv1a, false);
        probe *p = probe_new(M, hash_fnv1a, false);
        for (int i = 0; i < n; i++) chain_put(c, keys[i], i), probe_put(p, keys[i], i);
        double best[2] = {1e9, 1e9};
        for (int r = 0; r < 3; r++) {
            double t = now();
            for (int i = 0; i < n; i++) chain_get(c, keys[i], &v);
            t = now() - t, best[0] = t < best[0] ? t : best[0];
            t = now();
            for (int i = 0; i < n; i++) probe_get(p, keys[i], &v);
            t = now() - t, best[1] = t < best[1] ? t : best[1];
        }
        printf("%5.2f %10.1f %10.1f\n", alphas[a], 1e9 * best[0] / n, 1e9 * best[1] / n);
        chain_free(c), probe_free(p);
    }
    return 0;
}
