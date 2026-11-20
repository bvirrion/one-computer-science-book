// Exercise 8: search --count -- intersect the lists, shortest first, and only count.
#include <stdlib.h>
#include <string.h>

#include "exercises.h"

int count_and(const Index *ix, char **terms, int nterms) {
    const PostingList *shortest = NULL;
    for (int i = 0; i < nterms; i++) {
        const PostingList *l = index_lookup(ix, terms[i]);
        if (l == NULL)
            return 0;
        if (shortest == NULL || l->size < shortest->size)
            shortest = l;
    }
    int n = 0;
    for (int j = 0; j < shortest->size; j++) {  // a document of the shortest list...
        int doc = shortest->items[j].doc, all = 1;
        for (int i = 0; i < nterms && all; i++) {  // ...must be in every other list
            const PostingList *l = index_lookup(ix, terms[i]);
            int lo = 0, hi = l->size - 1, found = 0;
            while (lo <= hi && !found) {
                int mid = lo + (hi - lo) / 2;
                found = l->items[mid].doc == doc;
                if (l->items[mid].doc < doc)
                    lo = mid + 1;
                else
                    hi = mid - 1;
            }
            all = found;
        }
        n += all;
    }
    return n;
}
