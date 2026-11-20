// stack.c: a stack is a dynamic array used at one end only.
#include "stack.h"
#include "vec.h"
#include <stdlib.h>

struct stack {
    vec *items;  // the top is the last element
};

stack *stack_new(void) {
    stack *s = malloc(sizeof *s);
    if (s == NULL) exit(1);
    s->items = vec_new();
    return s;
}

void stack_free(stack *s) {
    vec_free(s->items);
    free(s);
}

bool stack_empty(const stack *s) { return vec_size(s->items) == 0; }
int stack_top(const stack *s) { return vec_get(s->items, vec_size(s->items) - 1); }
void stack_push(stack *s, int x) { vec_push(s->items, x); }
int stack_pop(stack *s) { return vec_pop(s->items); }
