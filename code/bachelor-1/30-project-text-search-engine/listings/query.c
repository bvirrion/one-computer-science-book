// query.c: intersect the posting lists, shortest first; score the survivors.
#include "query.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double tfidf(int ndocs, const int *tf, const int *df, int nterms) {
    double s = 0;
    for (int i = 0; i < nterms; i++)
        s += tf[i] * log((double)ndocs / df[i]);
    return s;
}

static int by_length(const void *a, const void *b) {
    return (*(const PostingList *const *)a)->size - (*(const PostingList *const *)b)->size;
}

static int count_in(const PostingList *l, int doc) {  // binary search: the list is sorted
    int lo = 0, hi = l->size - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (l->items[mid].doc == doc)
            return l->items[mid].count;
        if (l->items[mid].doc < doc)
            lo = mid + 1;
        else
            hi = mid - 1;
    }
    return 0;
}

int query_and(const Index *ix, char **terms, int nterms, Hit *top, int k, int *nfound) {
    const PostingList **lists = malloc(nterms * sizeof *lists);
    const PostingList **sorted = malloc(nterms * sizeof *sorted);
    int matches = -1, *docs = NULL, *tf = NULL, *df = NULL;  // -1: out of memory
    *nfound = 0;
    if (lists == NULL || sorted == NULL)
        goto done;
    matches = 0;
    for (int i = 0; i < nterms; i++)
        if ((lists[i] = sorted[i] = index_lookup(ix, terms[i])) == NULL)
            goto done;  // a word in no document: no document has them all
    qsort(sorted, nterms, sizeof *sorted, by_length);
    int n = sorted[0]->size;
    docs = malloc(n * sizeof *docs);
    tf = malloc(nterms * sizeof *tf);
    df = malloc(nterms * sizeof *df);
    if (docs == NULL || tf == NULL || df == NULL) {
        matches = -1;
        goto done;
    }
    for (int j = 0; j < n; j++)
        docs[j] = sorted[0]->items[j].doc;
    for (int i = 1; i < nterms && n > 0; i++) {  // merge: keep the docs also in list i
        int a = 0, b = 0, kept = 0;
        while (a < n && b < sorted[i]->size) {
            int d = sorted[i]->items[b].doc;
            if (docs[a] < d)
                a++;
            else if (docs[a] > d)
                b++;
            else
                docs[kept++] = docs[a++], b++;
        }
        n = kept;
    }
    TopK t;
    topk_init(&t, top, k);
    for (int j = 0; j < n; j++) {
        for (int i = 0; i < nterms; i++)
            tf[i] = count_in(lists[i], docs[j]), df[i] = lists[i]->size;
        topk_push(&t, (Hit){tfidf(ix->ndocs, tf, df, nterms), docs[j]});
    }
    *nfound = topk_sorted(&t);
    matches = n;
done:
    free(tf);
    free(df);
    free(docs);
    free(lists);
    free(sorted);
    return matches;
}

void print_hits(char **names, const Hit *top, int shown, int matches) {
    if (matches == 0) {
        printf("no document contains every word\n");
        return;
    }
    printf("%d document%s contain%s every word; the best %d:\n", matches,
           matches == 1 ? "" : "s", matches == 1 ? "s" : "", shown);
    for (int i = 0; i < shown; i++)
        printf("%9.4f  %s\n", top[i].score, names[top[i].doc]);
}
