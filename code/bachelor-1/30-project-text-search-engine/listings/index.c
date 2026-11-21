// index.c: chained hash table (FNV-1a) whose entries hold growing posting lists.
#define _POSIX_C_SOURCE 200809L
#include "index.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "folder.h"
#include "tokenize.h"

static uint64_t fnv1a(const char *s) {
    uint64_t h = 14695981039346656037u;
    for (; *s; s++)
        h = (h ^ (unsigned char)*s) * 1099511628211u;
    return h;
}

int index_init(Index *ix) {
    *ix = (Index){0};
    ix->buckets = calloc(1024, sizeof *ix->buckets);
    ix->nbuckets = ix->buckets != NULL ? 1024 : 0;
    return ix->buckets != NULL ? 0 : -1;
}

static void grow_table(Index *ix) {
    size_t n = 2 * ix->nbuckets;
    Entry **b = calloc(n, sizeof *b);
    if (b == NULL)
        return;  // no memory: keep the old table, slower but still correct
    for (size_t i = 0; i < ix->nbuckets; i++)
        for (Entry *e = ix->buckets[i], *next; e != NULL; e = next) {
            next = e->next;  // move e to its bucket in the new table
            size_t j = fnv1a(e->word) % n;
            e->next = b[j];
            b[j] = e;
        }
    free(ix->buckets);
    ix->buckets = b;
    ix->nbuckets = n;
}

static Entry *find_or_add(Index *ix, const char *word) {
    size_t i = fnv1a(word) % ix->nbuckets;
    for (Entry *e = ix->buckets[i]; e != NULL; e = e->next)
        if (strcmp(e->word, word) == 0)
            return e;
    Entry *e = calloc(1, sizeof *e);
    if (e == NULL || (e->word = strdup(word)) == NULL) {
        free(e);
        return NULL;  // out of memory
    }
    e->next = ix->buckets[i];
    ix->buckets[i] = e;
    if (++ix->nwords > ix->nbuckets)
        grow_table(ix);
    return e;
}

static int add_occurrence(Index *ix, PostingList *l, int doc) {
    if (l->size > 0 && l->items[l->size - 1].doc == doc) {
        l->items[l->size - 1].count++;  // the word again, in the same document
        return 0;
    }
    if (l->size == l->cap) {  // full: grow through a temporary, which may be NULL
        int cap = l->cap ? 2 * l->cap : 2;
        Posting *items = realloc(l->items, cap * sizeof *items);
        if (items == NULL)
            return -1;  // out of memory: the list is left as it was
        l->items = items;
        l->cap = cap;
    }
    l->items[l->size++] = (Posting){doc, 1};
    ix->npostings++;
    return 0;
}

int index_add_text(Index *ix, const char *name, const char *text, size_t len) {
    if (ix->ndocs == ix->cap_docs) {
        int cap = ix->cap_docs ? 2 * ix->cap_docs : 64;
        char **names = realloc(ix->names, cap * sizeof *names);
        if (names == NULL)
            return -1;
        ix->names = names;
        ix->cap_docs = cap;
    }
    char *copy = strdup(name);
    if (copy == NULL)
        return -1;
    int doc = ix->ndocs++;
    ix->names[doc] = copy;
    char word[MAX_WORD];
    size_t pos = 0;
    while (next_word(text, len, &pos, word) > 0) {
        Entry *e = find_or_add(ix, word);
        if (e == NULL || add_occurrence(ix, &e->list, doc) != 0)
            return -1;  // out of memory: the document is only partly indexed
    }
    return doc;
}

int index_directory(Index *ix, const char *dir) {
    Folder f;
    if (folder_list(&f, dir) != 0)
        return -1;
    int status = 0;
    for (int i = 0; i < f.n; i++) {
        char path[4096];
        size_t len;
        snprintf(path, sizeof path, "%s/%s", dir, f.names[i]);
        char *text = read_file(path, &len);
        if (text == NULL || index_add_text(ix, f.names[i], text, len) < 0)
            status = -1;
        free(text);
    }
    folder_free(&f);
    return status;
}

const PostingList *index_lookup(const Index *ix, const char *word) {
    for (Entry *e = ix->buckets[fnv1a(word) % ix->nbuckets]; e != NULL; e = e->next)
        if (strcmp(e->word, word) == 0)
            return &e->list;
    return NULL;
}

size_t index_memory(const Index *ix) {
    size_t bytes = ix->nbuckets * sizeof(Entry *) + ix->cap_docs * sizeof(char *);
    for (int d = 0; d < ix->ndocs; d++)
        bytes += strlen(ix->names[d]) + 1;
    for (size_t i = 0; i < ix->nbuckets; i++)
        for (Entry *e = ix->buckets[i]; e != NULL; e = e->next)
            bytes += sizeof *e + strlen(e->word) + 1 + e->list.cap * sizeof(Posting);
    return bytes;
}

void index_free(Index *ix) {
    for (size_t i = 0; i < ix->nbuckets; i++)
        for (Entry *e = ix->buckets[i], *next; e != NULL; e = next) {
            next = e->next;
            free(e->word);
            free(e->list.items);
            free(e);
        }
    for (int d = 0; d < ix->ndocs; d++)
        free(ix->names[d]);
    free(ix->names);
    free(ix->buckets);
}
