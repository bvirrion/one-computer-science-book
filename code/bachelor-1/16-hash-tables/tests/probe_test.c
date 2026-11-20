// test-with: ../listings/probe.c ../listings/hashes.c
// Linear probing with deletions and tombstones, resizing, and a cluster of equal hashes.
#include "probe.h"
#include "table_suite.h"

SUITE(probe, probe, probe_new(8, hash_fnv1a, true))

int main(void) {
    probe_suite();
    probe *t = probe_new(11, hash_first, false);  // every key in one cluster
    const char *k[] = {"a1", "a2", "a3", "a4", "a5"};
    for (int i = 0; i < 5; i++) probe_put(t, k[i], i);
    probe_delete(t, "a2");
    int v;
    assert(probe_get(t, "a5", &v) && v == 4);  // found past the tombstone
    probe_put(t, "a6", 6);                     // reuses the tombstone
    assert(probe_get(t, "a6", &v) && v == 6 && probe_size(t) == 5);
    probe_free(t);
    puts("probe: ok");
    return 0;
}
