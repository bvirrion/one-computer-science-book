// chain.h: a dictionary from strings to ints, by a hash table with separate chaining.
#ifndef CHAIN_H
#define CHAIN_H
#include "hashes.h"
#include <stdbool.h>
#include <stddef.h>

typedef struct chain chain;

chain *chain_new(size_t m, hash_fn h, bool resize);  // m buckets; resize: double when n > m
void chain_free(chain *t);
void chain_put(chain *t, const char *key, int value);  // insert or replace
bool chain_get(const chain *t, const char *key, int *value);
bool chain_delete(chain *t, const char *key);
size_t chain_size(const chain *t);
size_t chain_buckets(const chain *t);
size_t chain_length(const chain *t, size_t bucket);  // the length of one chain
long chain_compared(const chain *t);  // keys compared by the searches so far
#endif
