// wordfreq.c: the frequency of each word of standard input, with the chaining table;
// prints "word count" for each distinct word, in order of first appearance.
#include "chain.h"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    chain *t = chain_new(64, hash_fnv1a, true);
    static char order[20000][32];
    int distinct = 0, c, len = 0;
    char w[32];
    do {
        c = getchar();
        if (c != EOF && isalpha(c) && len < 31) {
            w[len++] = (char)tolower(c);
        } else if (len > 0) {
            w[len] = '\0', len = 0;
            int count = 0;
            if (!chain_get(t, w, &count)) snprintf(order[distinct++], 32, "%s", w);
            chain_put(t, w, count + 1);
        }
    } while (c != EOF);
    for (int i = 0; i < distinct; i++) {
        int count = 0;
        chain_get(t, order[i], &count);
        printf("%s %d\n", order[i], count);
    }
    chain_free(t);
    return 0;
}
