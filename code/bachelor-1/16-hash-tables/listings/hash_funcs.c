// hash_funcs.c: four hash values of a few keys, and their buckets among m = 31.
// capture: with=hashes.c
#include "hashes.h"
#include <stdio.h>

int main(void) {
    const char *keys[] = {"Emil Thornworth", "Quinn Woodwell", "listen", "silent", "Aa", "BB"};
    printf("%-16s %6s %6s %22s %22s\n", "key", "first", "sum", "polynomial", "FNV-1a");
    for (int i = 0; i < 6; i++) {
        const char *k = keys[i];
        printf("%-16s %6llu %6llu %22llu %22llu\n", k, (unsigned long long)hash_first(k),
               (unsigned long long)hash_additive(k), (unsigned long long)hash_poly(k),
               (unsigned long long)hash_fnv1a(k));
    }
    printf("\nbuckets, m = 31 (the hash value mod 31):\n");
    for (int i = 0; i < 6; i++) {
        const char *k = keys[i];
        printf("%-16s %6llu %6llu %22llu %22llu\n", k,
               (unsigned long long)(hash_first(k) % 31),
               (unsigned long long)(hash_additive(k) % 31),
               (unsigned long long)(hash_poly(k) % 31),
               (unsigned long long)(hash_fnv1a(k) % 31));
    }
    return 0;
}
