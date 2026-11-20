// phonebook_v0.c: the first version, with three of the five planted memory errors.
#include <stdlib.h>
#include <string.h>
#include "phonebook.h"

void book_init(struct book *b, int policy)
{
    b->items = NULL;
    b->len = b->cap = 0;
    b->policy = policy;
    b->copies = 0;
}

static size_t next_capacity(const struct book *b)
{
    if (b->policy > 0)
        return b->cap + (size_t)b->policy;
    size_t cap = (b->cap * (size_t)(-b->policy) + 1) / 2;   // x2, or x1.5 rounded up
    return cap > b->cap ? cap : b->cap + 1;
}

int book_add(struct book *b, const char *name, long number)
{
    if (b->len == b->cap) {
        size_t cap = next_capacity(b);
        struct contact *bigger = malloc(cap * sizeof *bigger);
        if (bigger == NULL)
            return -1;
        for (size_t i = 0; i < b->len; i++)
            bigger[i] = b->items[i];
        b->copies += (long)b->len;
        free(b->items);
        b->items = bigger;
        b->cap = cap;
    }
    char *copy = malloc(strlen(name));                  // error 1
    if (copy == NULL)
        return -1;
    strcpy(copy, name);
    b->items[b->len].name = copy;
    b->items[b->len].number = number;
    b->len++;
    return 0;
}

const struct contact *book_find(const struct book *b, const char *name)
{
    for (size_t i = 0; i < b->len; i++)
        if (strcmp(b->items[i].name, name) == 0)
            return &b->items[i];
    return NULL;
}

int book_remove(struct book *b, const char *name)
{
    for (size_t i = 0; i < b->len; i++)
        if (strcmp(b->items[i].name, name) == 0) {
            free(b->items[i].name);                     // the book owned it
            b->items[i] = b->items[b->len];             // error 2
            b->len--;
            return 0;
        }
    return -1;
}

void book_destroy(struct book *b)
{
    free(b->items);                                     // error 3
    book_init(b, b->policy);
}
