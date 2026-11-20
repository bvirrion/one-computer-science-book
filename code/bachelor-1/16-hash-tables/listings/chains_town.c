// chains_town.c: the 120 names of the town in tables of m buckets, under four hashes.
// capture: with=chain.c,probe.c,hashes.c
#include "chain.h"
#include "probe.h"
#include "town_names.h"

static const char *names[] = {"first", "additive", "polynomial", "FNV-1a"};
static const hash_fn fns[] = {hash_first, hash_additive, hash_poly, hash_fnv1a};

int main(void) {
    read_town_names();
    printf("chaining: longest chain / empty buckets / keys compared per successful search\n");
    printf("%-11s %15s %15s %15s\n", "", "m = 31", "m = 64", "m = 127");
    for (int f = 0; f < 4; f++) {
        printf("%-11s", names[f]);
        for (int j = 0; j < 3; j++) {
            size_t m = j == 0 ? 31 : j == 1 ? 64 : 127;
            chain *t = chain_new(m, fns[f], false);
            for (int i = 0; i < PEOPLE; i++) chain_put(t, town_names[i], i);
            size_t longest = 0, empty = 0;
            for (size_t b = 0; b < m; b++) {
                size_t len = chain_length(t, b);
                longest = len > longest ? len : longest;
                empty += len == 0;
            }
            long before = chain_compared(t);
            int v;
            for (int i = 0; i < PEOPLE; i++) chain_get(t, town_names[i], &v);
            printf("   %3zu %3zu %6.2f", longest, empty,
                   (double)(chain_compared(t) - before) / PEOPLE);
            chain_free(t);
        }
        printf("\n");
    }
    printf("linear probing: slots probed per successful search\n");
    printf("%-11s %9s %9s\n", "", "m = 127", "m = 251");
    for (int f = 0; f < 4; f++) {
        printf("%-11s", names[f]);
        for (size_t m = 127; m <= 251; m += 124) {
            probe *t = probe_new(m, fns[f], false);
            for (int i = 0; i < PEOPLE; i++) probe_put(t, town_names[i], i);
            long before = probe_probes(t);
            int v;
            for (int i = 0; i < PEOPLE; i++) probe_get(t, town_names[i], &v);
            printf(" %9.2f", (double)(probe_probes(t) - before) / PEOPLE);
            probe_free(t);
        }
        printf("\n");
    }
    return 0;
}
