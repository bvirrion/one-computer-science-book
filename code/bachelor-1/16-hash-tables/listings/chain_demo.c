// chain_demo.c: counting words with a dictionary.
// capture: with=chain.c,hashes.c
#include "chain.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    char text[] = "the cat saw the dog and the dog saw the cat run to the river";
    chain *t = chain_new(7, hash_fnv1a, false);
    for (char *w = strtok(text, " "); w != NULL; w = strtok(NULL, " ")) {
        int count = 0;
        chain_get(t, w, &count);  // 0 if absent
        chain_put(t, w, count + 1);
    }
    const char *show[] = {"the", "cat", "dog", "river", "fish"};
    for (int i = 0; i < 5; i++) {
        int c = 0;
        printf("%-6s %d\n", show[i], chain_get(t, show[i], &c) ? c : 0);
    }
    printf("%zu keys in %zu buckets, chain lengths:", chain_size(t), chain_buckets(t));
    for (size_t b = 0; b < chain_buckets(t); b++) printf(" %zu", chain_length(t, b));
    printf("\n");
    chain_delete(t, "the");
    printf("after deleting \"the\": %zu keys\n", chain_size(t));
    chain_free(t);
    return 0;
}
