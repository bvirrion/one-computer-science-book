// intvec.c: push doubles the capacity when the block is full.
#include <stdlib.h>
#include "intvec.h"

void intvec_init(struct intvec *v)
{
    v->data = NULL;
    v->len = v->cap = 0;
    v->copies = 0;
}

int intvec_push(struct intvec *v, int x)
{
    if (v->len == v->cap) {                         // full: move to a block twice as big
        size_t cap = v->cap == 0 ? 1 : 2 * v->cap;
        int *bigger = malloc(cap * sizeof *bigger);
        if (bigger == NULL)
            return -1;                              // v is unchanged
        for (size_t i = 0; i < v->len; i++)
            bigger[i] = v->data[i];                 // the copies that growth costs
        v->copies += (long)v->len;
        free(v->data);
        v->data = bigger;
        v->cap = cap;
    }
    v->data[v->len++] = x;
    return 0;
}

void intvec_free(struct intvec *v)
{
    free(v->data);
    intvec_init(v);
}
