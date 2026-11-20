// hashes.h: four hash functions from strings to 64-bit hash values.
#ifndef HASHES_H
#define HASHES_H
#include <stdint.h>

typedef uint64_t (*hash_fn)(const char *s);

uint64_t hash_first(const char *s);     // the first character only
uint64_t hash_additive(const char *s);  // the sum of the characters
uint64_t hash_poly(const char *s);      // s[0]*31^(L-1) + ... + s[L-1], mod 2^64
uint64_t hash_fnv1a(const char *s);     // FNV-1a, 64 bits
uint64_t hash_fnv1a_seeded(const char *s, uint64_t seed);
#endif
