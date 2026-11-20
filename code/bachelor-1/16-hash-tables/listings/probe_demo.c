// probe_demo.c: linear probing in 11 slots, keyed by the first letter (to see collisions).
// capture: with=probe.c,hashes.c
#include "probe.h"
#include <stdio.h>

int main(void) {
    probe *t = probe_new(11, hash_first, false);
    const char *names[] = {"Ada", "Bo", "Lea", "Al", "Cy", "Bea", "Wes"};
    for (int i = 0; i < 7; i++) {
        probe_put(t, names[i], i);
        printf("put %-4s (hash %3d mod 11 = %2d)  ", names[i], names[i][0], names[i][0] % 11);
        probe_show(t);
    }
    probe_delete(t, "Bo");
    printf("delete Bo                         ");
    probe_show(t);
    int v = -1;
    long before = probe_probes(t);
    bool found = probe_get(t, "Bea", &v);
    printf("get Bea: %s, value %d, %ld probes\n", found ? "found" : "absent", v,
           probe_probes(t) - before);
    probe_free(t);
    return 0;
}
