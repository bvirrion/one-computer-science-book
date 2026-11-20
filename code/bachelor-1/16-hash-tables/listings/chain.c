// chain.c: each bucket is a singly linked list of (key, value) cells.
#include "chain.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct entry {
    char *key;
    int value;
    struct entry *next;
} entry;

struct chain {
    entry **buckets;  // m list heads
    size_t m, n;
    hash_fn h;
    bool resize;
    long compared;
};

static void *checked(void *p) {
    if (p == NULL) {
        perror("chain");
        exit(1);
    }
    return p;
}

static char *copy(const char *s) {  // strdup is not in C17
    return strcpy(checked(malloc(strlen(s) + 1)), s);
}

chain *chain_new(size_t m, hash_fn h, bool resize) {
    chain *t = checked(malloc(sizeof *t));
    *t = (chain){checked(calloc(m, sizeof(entry *))), m, 0, h, resize, 0};
    return t;
}

static entry **find(chain *t, const char *key) {  // the link to the key's cell, or to NULL
    entry **link = &t->buckets[t->h(key) % t->m];
    while (*link != NULL) {
        t->compared++;
        if (strcmp((*link)->key, key) == 0) break;
        link = &(*link)->next;
    }
    return link;
}

static void grow(chain *t) {  // rehash every cell into twice as many buckets
    chain bigger = {checked(calloc(2 * t->m, sizeof(entry *))), 2 * t->m, t->n, t->h, true, 0};
    for (size_t b = 0; b < t->m; b++)
        for (entry *e = t->buckets[b], *next; e != NULL; e = next) {
            next = e->next;
            entry **head = &bigger.buckets[t->h(e->key) % bigger.m];
            e->next = *head;
            *head = e;
        }
    free(t->buckets);
    bigger.compared = t->compared;
    *t = bigger;
}

void chain_put(chain *t, const char *key, int value) {
    entry **link = find(t, key);
    if (*link != NULL) {
        (*link)->value = value;
        return;
    }
    entry *e = checked(malloc(sizeof *e));
    *e = (entry){copy(key), value, NULL};
    *link = e;  // at the end of its chain
    if (++t->n > t->m && t->resize) grow(t);
}

bool chain_get(const chain *t, const char *key, int *value) {
    entry *e = *find((chain *)t, key);
    if (e != NULL) *value = e->value;
    return e != NULL;
}

bool chain_delete(chain *t, const char *key) {
    entry **link = find(t, key);
    if (*link == NULL) return false;
    entry *dead = *link;
    *link = dead->next;
    free(dead->key);
    free(dead);
    t->n--;
    return true;
}

size_t chain_size(const chain *t) { return t->n; }
size_t chain_buckets(const chain *t) { return t->m; }
long chain_compared(const chain *t) { return t->compared; }

size_t chain_length(const chain *t, size_t bucket) {
    size_t n = 0;
    for (entry *e = t->buckets[bucket]; e != NULL; e = e->next) n++;
    return n;
}

void chain_free(chain *t) {
    for (size_t b = 0; b < t->m; b++)
        for (entry *e = t->buckets[b], *next; e != NULL; e = next) {
            next = e->next;
            free(e->key);
            free(e);
        }
    free(t->buckets);
    free(t);
}
