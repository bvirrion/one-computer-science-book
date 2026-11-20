// stack.c: a growable array behind an opaque type.
#include <stdlib.h>
#include "stack.h"

struct stack {
    int *data;
    size_t len, cap;
};

struct stack *stack_new(void)
{
    return calloc(1, sizeof(struct stack));
}

void stack_free(struct stack *s)
{
    if (s != NULL)
        free(s->data);
    free(s);
}

int stack_push(struct stack *s, int v)
{
    if (s->len == s->cap) {
        size_t cap = s->cap == 0 ? 4 : 2 * s->cap;
        int *bigger = realloc(s->data, cap * sizeof *bigger);
        if (bigger == NULL)
            return -1;
        s->data = bigger;
        s->cap = cap;
    }
    s->data[s->len++] = v;
    return 0;
}

int stack_pop(struct stack *s, int *v)
{
    if (s->len == 0)
        return -1;
    *v = s->data[--s->len];
    return 0;
}

size_t stack_size(const struct stack *s) { return s->len; }
