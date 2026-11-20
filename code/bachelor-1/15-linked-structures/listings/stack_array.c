// stack_array.c: a stack on a doubling array; the top is the last element.
#include "stack.h"
#include <stdlib.h>

struct stack {
    int *data;
    size_t size, capacity;
};

stack *stack_new(void) {
    stack *s = malloc(sizeof *s);
    int *data = malloc(sizeof *data);
    if (s == NULL || data == NULL) exit(1);
    *s = (stack){data, 0, 1};
    return s;
}

void stack_free(stack *s) {
    free(s->data);
    free(s);
}

bool stack_empty(const stack *s) { return s->size == 0; }
int stack_top(const stack *s) { return s->data[s->size - 1]; }
int stack_pop(stack *s) { return s->data[--s->size]; }
const char *stack_kind(void) { return "an array"; }

void stack_push(stack *s, int x) {
    if (s->size == s->capacity) {
        int *data = realloc(s->data, 2 * s->capacity * sizeof *data);
        if (data == NULL) exit(1);
        s->data = data;
        s->capacity *= 2;
    }
    s->data[s->size++] = x;
}
