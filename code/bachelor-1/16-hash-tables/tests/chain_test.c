// test-with: ../listings/chain.c ../listings/hashes.c
// The chaining table, with and without resizing; FNV-1a against a published value.
#include "chain.h"
#include "table_suite.h"

SUITE(chain, chain, chain_new(13, hash_fnv1a, true))

int main(void) {
    assert(hash_fnv1a("") == 0xcbf29ce484222325u && hash_fnv1a("a") == 0xaf63dc4c8601ec8cu);
    assert(hash_poly("Aa") == hash_poly("BB") && hash_additive("listen") == hash_additive("silent"));
    chain_suite();
    chain *t = chain_new(4, hash_additive, false);  // no resizing: chains grow
    char key[8];
    for (int i = 0; i < 100; i++) snprintf(key, sizeof key, "%d", i), chain_put(t, key, i);
    size_t total = 0;
    for (size_t b = 0; b < 4; b++) total += chain_length(t, b);
    assert(total == 100 && chain_buckets(t) == 4);
    chain_free(t);
    puts("chain: ok");
    return 0;
}
