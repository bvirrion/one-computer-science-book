// attack.c: "Aa" and "BB" have the same polynomial hash, so every string made of
// k such blocks has it too: 2^k keys, one hash value. A seeded hash spreads them.
// capture: with=hashes.c
#include "hashes.h"
#include <stdio.h>

int main(void) {
    int k = 10, n = 1 << k;
    static char keys[1 << 10][21];
    for (int x = 0; x < n; x++) {
        for (int i = 0; i < k; i++) {
            const char *block = (x >> i & 1) ? "BB" : "Aa";
            keys[x][2 * i] = block[0], keys[x][2 * i + 1] = block[1];
        }
        keys[x][2 * k] = '\0';
    }
    printf("%s %s ... %s\n", keys[0], keys[1], keys[n - 1]);
    int same = 0;
    for (int x = 0; x < n; x++) same += hash_poly(keys[x]) == hash_poly(keys[0]);
    printf("%d keys, %d with the polynomial hash %llu\n", n, same,
           (unsigned long long)hash_poly(keys[0]));
    for (uint64_t seed = 0; seed <= 2; seed++) {  // m = 1021 buckets
        static int bucket[1021];
        int used = 0;
        for (int b = 0; b < 1021; b++) bucket[b] = 0;
        for (int x = 0; x < n; x++) used += bucket[hash_fnv1a_seeded(keys[x], seed) % 1021]++ == 0;
        printf("FNV-1a, seed %llu: %d of 1021 buckets used; the first key in bucket %llu\n",
               (unsigned long long)seed, used,
               (unsigned long long)(hash_fnv1a_seeded(keys[0], seed) % 1021));
    }
    return 0;
}
