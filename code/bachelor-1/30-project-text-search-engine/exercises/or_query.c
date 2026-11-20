// Exercise 7: OR queries -- merge the posting lists instead of intersecting them.
#include <math.h>
#include <stdlib.h>

#include "exercises.h"

int query_or(const Index *ix, char **terms, int nterms, Hit *top, int k, int *nfound) {
    double *score = calloc(ix->ndocs, sizeof *score);  // a score per document: simple
    char *seen = calloc(ix->ndocs, 1);
    for (int i = 0; i < nterms; i++) {
        const PostingList *l = index_lookup(ix, terms[i]);
        for (int j = 0; l != NULL && j < l->size; j++) {
            score[l->items[j].doc] += l->items[j].count * log((double)ix->ndocs / l->size);
            seen[l->items[j].doc] = 1;
        }
    }
    TopK t;
    topk_init(&t, top, k);
    int matches = 0;
    for (int d = 0; d < ix->ndocs; d++)
        if (seen[d]) {
            matches++;
            topk_push(&t, (Hit){score[d], d});
        }
    *nfound = topk_sorted(&t);
    free(score);
    free(seen);
    return matches;
}
