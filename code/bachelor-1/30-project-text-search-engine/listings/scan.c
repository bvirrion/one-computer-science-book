// scan.c: count every term in every file, then score the files that have them all.
#include "scan.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "query.h"
#include "tokenize.h"

int scan_and(const char *dir, const Folder *f, char **terms, int nterms, Hit *top, int k,
             int *nfound) {
    int *tf = calloc((size_t)f->n * nterms, sizeof *tf), *df = calloc(nterms, sizeof *df);
    if (tf == NULL || df == NULL) {  // out of memory
        free(tf);
        free(df);
        return -1;
    }
    for (int d = 0; d < f->n; d++) {
        char path[4096], word[MAX_WORD];
        size_t len, pos = 0;
        snprintf(path, sizeof path, "%s/%s", dir, f->names[d]);
        char *text = read_file(path, &len);
        while (text != NULL && next_word(text, len, &pos, word) > 0)
            for (int i = 0; i < nterms; i++)
                tf[d * nterms + i] += strcmp(word, terms[i]) == 0;
        free(text);
        for (int i = 0; i < nterms; i++)
            df[i] += tf[d * nterms + i] > 0;
    }
    TopK t;
    topk_init(&t, top, k);
    int matches = 0;
    for (int d = 0; d < f->n; d++) {
        int all = 1;
        for (int i = 0; i < nterms; i++)
            all = all && tf[d * nterms + i] > 0;
        if (all) {
            matches++;
            topk_push(&t, (Hit){tfidf(f->n, &tf[d * nterms], df, nterms), d});
        }
    }
    *nfound = topk_sorted(&t);
    free(tf);
    free(df);
    return matches;
}
