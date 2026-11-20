// hashes.c: the four hash functions; unsigned arithmetic wraps modulo 2^64.
#include "hashes.h"

uint64_t hash_first(const char *s) { return (unsigned char)s[0]; }

uint64_t hash_additive(const char *s) {
    uint64_t h = 0;
    for (; *s; s++) h += (unsigned char)*s;
    return h;
}

uint64_t hash_poly(const char *s) {
    uint64_t h = 0;
    for (; *s; s++) h = 31 * h + (unsigned char)*s;  // Horner's scheme
    return h;
}

uint64_t hash_fnv1a_seeded(const char *s, uint64_t seed) {
    uint64_t h = 14695981039346656037u ^ seed;  // the offset basis
    for (; *s; s++) {
        h ^= (unsigned char)*s;  // first mix in the byte,
        h *= 1099511628211u;     // then multiply by the FNV prime
    }
    return h;
}

uint64_t hash_fnv1a(const char *s) { return hash_fnv1a_seeded(s, 0); }
