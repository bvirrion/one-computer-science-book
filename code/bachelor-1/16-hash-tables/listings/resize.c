// resize.c: inserting n keys into an open-addressing table that doubles when 3/4 full:
// how many keys do the rehashes move?
// capture: with=probe.c,hashes.c
#include "probe.h"
#include <stdio.h>

int main(void) {
    printf("%8s %10s %10s %8s\n", "n", "moves", "moves/n", "slots");
    for (int n = 1000; n <= 1000000; n *= 10) {
        long moves = 0;
        size_t m = 8, used = 0;  // the same rule as probe_put, counted without the table
        for (int i = 0; i < n; i++) {
            used++;
            if (4 * used > 3 * m) moves += (long)used, m *= 2;
        }
        printf("%8d %10ld %10.3f %8zu\n", n, moves, (double)moves / n, m);
    }
    probe *t = probe_new(8, hash_fnv1a, true);  // and a real table, to check the rule
    char key[16];
    for (int i = 0; i < 1000; i++) snprintf(key, sizeof key, "k%d", i), probe_put(t, key, i);
    int v, ok = 0;
    for (int i = 0; i < 1000; i++) snprintf(key, sizeof key, "k%d", i), ok += probe_get(t, key, &v) && v == i;
    printf("a real table holds %zu keys, %d found again\n", probe_size(t), ok);
    probe_free(t);
    return 0;
}
