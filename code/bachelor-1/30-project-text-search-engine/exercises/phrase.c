// Exercise 10: phrase queries with positions -- a positional index of the texts,
// then the phrase w1 w2 ... wk is found where w1 at p, w2 at p + 1, ..., wk at p + k - 1.
#include <stdlib.h>
#include <string.h>

#include "../listings/tokenize.h"
#include "exercises.h"

typedef struct {
    int doc, pos;
} Place;

static int places_of(const char **texts, int ndocs, const char *word, Place **out) {
    int n = 0, cap = 16;
    Place *p = malloc(cap * sizeof *p);
    for (int d = 0; d < ndocs; d++) {
        char w[MAX_WORD];
        size_t at = 0, len = strlen(texts[d]);
        for (int pos = 0; next_word(texts[d], len, &at, w) > 0; pos++)
            if (strcmp(w, word) == 0) {
                if (n == cap)
                    p = realloc(p, (cap *= 2) * sizeof *p);
                p[n++] = (Place){d, pos};  // sorted by (doc, pos), as they come
            }
    }
    *out = p;
    return n;
}

int phrase_docs(const char **texts, int ndocs, char **words, int nwords, int *docs) {
    Place *start;
    int n = places_of(texts, ndocs, words[0], &start), ndone = 0;
    for (int i = 1; i < nwords; i++) {  // keep the starts followed by word i at +i
        Place *next;
        int m = places_of(texts, ndocs, words[i], &next), a = 0, b = 0, kept = 0;
        while (a < n && b < m) {
            Place want = {start[a].doc, start[a].pos + i};
            if (want.doc < next[b].doc || (want.doc == next[b].doc && want.pos < next[b].pos))
                a++;
            else if (want.doc == next[b].doc && want.pos == next[b].pos)
                start[kept++] = start[a++], b++;
            else
                b++;
        }
        n = kept;
        free(next);
    }
    for (int j = 0; j < n; j++)
        if (ndone == 0 || docs[ndone - 1] != start[j].doc)
            docs[ndone++] = start[j].doc;
    free(start);
    return ndone;
}
