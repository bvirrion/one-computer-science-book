// Exercise 12: save the index in a binary file and load it back. The format: the
// number of documents and their names, then each word with its posting list; every
// number an int, every string its length then its bytes.
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "exercises.h"

static int put_int(FILE *f, int v) { return fwrite(&v, sizeof v, 1, f) == 1; }
static int get_int(FILE *f, int *v) { return fread(v, sizeof *v, 1, f) == 1; }

static int put_str(FILE *f, const char *s) {
    int n = (int)strlen(s);
    return put_int(f, n) && fwrite(s, 1, n, f) == (size_t)n;
}

static char *get_str(FILE *f) {
    int n;
    if (!get_int(f, &n) || n < 0 || n > 4096)
        return NULL;
    char *s = malloc(n + 1);
    if (s == NULL || fread(s, 1, n, f) != (size_t)n) {
        free(s);
        return NULL;
    }
    s[n] = '\0';
    return s;
}

int index_save(const Index *ix, const char *path) {
    FILE *f = fopen(path, "wb");
    int ok = f != NULL && put_int(f, ix->ndocs);
    for (int d = 0; ok && d < ix->ndocs; d++)
        ok = put_str(f, ix->names[d]);
    ok = ok && put_int(f, (int)ix->nwords);
    for (size_t b = 0; ok && b < ix->nbuckets; b++)
        for (Entry *e = ix->buckets[b]; ok && e != NULL; e = e->next) {
            ok = put_str(f, e->word) && put_int(f, e->list.size) &&
                 fwrite(e->list.items, sizeof(Posting), e->list.size, f) ==
                     (size_t)e->list.size;
        }
    if (f != NULL && fclose(f) != 0)
        ok = 0;
    return ok ? 0 : -1;
}

typedef struct {
    char *text;
    size_t len, cap;
} Buffer;

static int append(Buffer *b, const char *word) {  // word and a space; 0, or -1: no memory
    size_t n = strlen(word);
    if (b->len + n + 1 >= b->cap) {
        size_t cap = 2 * (b->len + n + 1);
        char *text = realloc(b->text, cap);
        if (text == NULL)
            return -1;
        b->text = text;
        b->cap = cap;
    }
    memcpy(b->text + b->len, word, n);
    b->len += n;
    b->text[b->len++] = ' ';
    return 0;
}

// Rebuild each document as its words, each repeated count times, and index those
// texts in document order: the same lists, counts and numbering as before.
int index_load(Index *ix, const char *path) {
    FILE *f = fopen(path, "rb");
    int n = 0, nwords, ok = f != NULL && get_int(f, &n) && n >= 0;
    char **names = calloc(n > 0 ? n : 1, sizeof *names);
    Buffer *docs = calloc(n > 0 ? n : 1, sizeof *docs);
    ok = ok && names != NULL && docs != NULL;
    for (int d = 0; ok && d < n; d++)
        ok = (names[d] = get_str(f)) != NULL;
    ok = ok && get_int(f, &nwords);
    for (int w = 0; ok && w < nwords; w++) {
        char *word = get_str(f);
        int size;
        ok = word != NULL && get_int(f, &size) && size > 0;
        Posting p;
        for (int j = 0; ok && j < size; j++) {
            ok = fread(&p, sizeof p, 1, f) == 1 && p.doc >= 0 && p.doc < n && p.count > 0;
            for (int c = 0; ok && c < p.count; c++)
                ok = append(&docs[p.doc], word) == 0;
        }
        free(word);
    }
    if (f != NULL)
        fclose(f);
    ok = index_init(ix) == 0 && ok;
    for (int d = 0; names != NULL && docs != NULL && d < n; d++) {
        if (ok)
            ok = index_add_text(ix, names[d], docs[d].text ? docs[d].text : "", docs[d].len) >= 0;
        free(names[d]);
        free(docs[d].text);
    }
    free(names);
    free(docs);
    return ok ? 0 : -1;
}
