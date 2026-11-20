// stack_list.c: a stack on a singly linked list; the top is the first cell.
#include "stack.h"
#include <stdlib.h>

typedef struct cell {
    int value;
    struct cell *next;
} cell;

struct stack {
    cell *top;
};

stack *stack_new(void) {
    stack *s = malloc(sizeof *s);
    if (s == NULL) exit(1);
    s->top = NULL;
    return s;
}

void stack_free(stack *s) {
    while (!stack_empty(s)) stack_pop(s);
    free(s);
}

bool stack_empty(const stack *s) { return s->top == NULL; }
int stack_top(const stack *s) { return s->top->value; }
const char *stack_kind(void) { return "a linked list"; }

void stack_push(stack *s, int x) {
    cell *c = malloc(sizeof *c);
    if (c == NULL) exit(1);
    *c = (cell){x, s->top};
    s->top = c;
}

int stack_pop(stack *s) {
    cell *c = s->top;
    int x = c->value;
    s->top = c->next;
    free(c);
    return x;
}
