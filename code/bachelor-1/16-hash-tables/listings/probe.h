// probe.h: the same dictionary by open addressing with linear probing.
#ifndef PROBE_H
#define PROBE_H
#include "hashes.h"
#include <stdbool.h>
#include <stddef.h>

typedef struct probe probe;

probe *probe_new(size_t m, hash_fn h, bool resize);  // resize: double when (n + dead) > 3m/4
void probe_free(probe *t);
void probe_put(probe *t, const char *key, int value);  // precondition without resize: a free slot
bool probe_get(const probe *t, const char *key, int *value);
bool probe_delete(probe *t, const char *key);
size_t probe_size(const probe *t);
long probe_probes(const probe *t);  // slots examined by the searches so far
void probe_show(const probe *t);    // one character per slot: . free, x tombstone, key's initial
#endif
