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

void index_init(Index *ix) {
    *ix = (Index){0};
    ix->nbuckets = 1024;
    ix->buckets = calloc(ix->nbuckets, sizeof *ix->buckets);
}

static void grow_table(Index *ix) {
    size_t n = 2 * ix->nbuckets;
    Entry **b = calloc(n, sizeof *b);
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
    e->word = strdup(word);
    e->next = ix->buckets[i];
    ix->buckets[i] = e;
    if (++ix->nwords > ix->nbuckets)
        grow_table(ix);
    return e;
}

static void add_occurrence(Index *ix, PostingList *l, int doc) {
    if (l->size > 0 && l->items[l->size - 1].doc == doc) {
        l->items[l->size - 1].count++;  // the word again, in the same document
        return;
    }
    if (l->size == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 2;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->size++] = (Posting){doc, 1};
    ix->npostings++;
}

int index_add_text(Index *ix, const char *name, const char *text, size_t len) {
    if (ix->ndocs == ix->cap_docs) {
        ix->cap_docs = ix->cap_docs ? 2 * ix->cap_docs : 64;
        ix->names = realloc(ix->names, ix->cap_docs * sizeof *ix->names);
    }
    int doc = ix->ndocs++;
    ix->names[doc] = strdup(name);
    char word[MAX_WORD];
    size_t pos = 0;
    while (next_word(text, len, &pos, word) > 0)
        add_occurrence(ix, &find_or_add(ix, word)->list, doc);
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
        if (text == NULL)
            status = -1;
        else
            index_add_text(ix, f.names[i], text, len);
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
