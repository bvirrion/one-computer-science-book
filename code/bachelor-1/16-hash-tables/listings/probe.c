// probe.c: one array of slots; a collision moves on to the next slot, cyclically.
#include "probe.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum state { FREE, USED, DEAD };  // DEAD: a tombstone left by a deletion

typedef struct {
    enum state state;
    char *key;
    int value;
} slot;

struct probe {
    slot *slots;
    size_t m, n, dead;
    hash_fn h;
    bool resize;
    long probes;
};

static void *checked(void *p) {
    if (p == NULL) {
        perror("probe");
        exit(1);
    }
    return p;
}

probe *probe_new(size_t m, hash_fn h, bool resize) {
    probe *t = checked(malloc(sizeof *t));
    *t = (probe){checked(calloc(m, sizeof(slot))), m, 0, 0, h, resize, 0};  // all FREE
    return t;
}

// the slot holding key, or else the first reusable slot met (tombstone or free)
static size_t find(probe *t, const char *key, bool *found) {
    size_t i = t->h(key) % t->m, reusable = t->m;
    for (size_t step = 0; step < t->m; step++, i = (i + 1) % t->m) {
        t->probes++;
        slot *s = &t->slots[i];
        if (s->state == FREE) break;  // the key is not further on
        if (s->state == DEAD) {
            if (reusable == t->m) reusable = i;
        } else if (strcmp(s->key, key) == 0) {
            *found = true;
            return i;
        }
    }
    *found = false;
    return reusable < t->m ? reusable : i;
}

static void grow(probe *t) {
    probe old = *t;
    *t = (probe){checked(calloc(2 * old.m, sizeof(slot))), 2 * old.m, 0, 0, old.h, true,
                 old.probes};
    for (size_t i = 0; i < old.m; i++)
        if (old.slots[i].state == USED) {
            probe_put(t, old.slots[i].key, old.slots[i].value);
            free(old.slots[i].key);
        }
    free(old.slots);
}

void probe_put(probe *t, const char *key, int value) {
    bool found;
    size_t i = find(t, key, &found);
    slot *s = &t->slots[i];
    if (!found) {
        if (s->state == DEAD) t->dead--;
        s->key = strcpy(checked(malloc(strlen(key) + 1)), key);
        s->state = USED;
        t->n++;
    }
    s->value = value;
    if (t->resize && 4 * (t->n + t->dead) > 3 * t->m) grow(t);
}

bool probe_get(const probe *t, const char *key, int *value) {
    bool found;
    size_t i = find((probe *)t, key, &found);
    if (found) *value = t->slots[i].value;
    return found;
}

bool probe_delete(probe *t, const char *key) {
    bool found;
    size_t i = find(t, key, &found);
    if (!found) return false;
    free(t->slots[i].key);
    t->slots[i].state = DEAD;  // not FREE: a search must go on past it
    t->n--, t->dead++;
    return true;
}

size_t probe_size(const probe *t) { return t->n; }
long probe_probes(const probe *t) { return t->probes; }

void probe_show(const probe *t) {
    for (size_t i = 0; i < t->m; i++) {
        const slot *s = &t->slots[i];
        putchar(s->state == FREE ? '.' : s->state == DEAD ? 'x' : s->key[0]);
    }
    putchar('\n');
}

void probe_free(probe *t) {
    for (size_t i = 0; i < t->m; i++)
        if (t->slots[i].state == USED) free(t->slots[i].key);
    free(t->slots);
    free(t);
}
