/* dict.h: a word counter, a hash table with open addressing (linear probing), grown at half full. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

struct slot { char *word; int count; };            /* word == NULL: an empty slot */
struct dict { struct slot *slots; size_t cap, len; };

static uint64_t hash(const char *s)                /* FNV-1a, 64 bits */
{
    uint64_t h = 14695981039346656037u;
    for (; *s; s++)
        h = (h ^ (unsigned char)*s) * 1099511628211u;
    return h;
}

static void dict_init(struct dict *d, size_t cap)  /* cap: a power of two */
{
    d->slots = calloc(cap, sizeof *d->slots);
    d->cap = cap;
    d->len = 0;
}

static void grow(struct dict *d)                   /* a new table twice as large; the slots move */
{
    struct dict bigger;
    dict_init(&bigger, 2 * d->cap);
    for (size_t i = 0; i < d->cap; i++)
        if (d->slots[i].word) {
            size_t j = hash(d->slots[i].word) & (bigger.cap - 1);
            while (bigger.slots[j].word)
                j = (j + 1) & (bigger.cap - 1);
            bigger.slots[j] = d->slots[i];
            bigger.len++;
        }
    free(d->slots);
    *d = bigger;
}

static size_t find(const struct dict *d, const char *word)   /* its slot, or the empty slot it would take */
{
    size_t i = hash(word) & (d->cap - 1);
    while (d->slots[i].word && strcmp(d->slots[i].word, word) != 0)
        i = (i + 1) & (d->cap - 1);
    return i;
}

/* The counter of word, created at 0 if missing. The pointer is valid until the next insertion. */
static int *dict_count(struct dict *d, const char *word)
{
    size_t i = find(d, word);
    if (!d->slots[i].word) {
        if (2 * (d->len + 1) > d->cap) {           /* a new word, and the table is half full */
            grow(d);
            i = find(d, word);
        }
#if BUG == 3
        d->slots[i].word = (char *)word;           /* BUG 3: keeps the caller's pointer */
#else
        d->slots[i].word = strdup(word);           /* the table owns its own copy */
#endif
        d->len++;
    }
    return &d->slots[i].count;
}

static void dict_free(struct dict *d)
{
    for (size_t i = 0; i < d->cap; i++)
#if BUG == 3
        (void)0;
#else
        free(d->slots[i].word);
#endif
    free(d->slots);
}
