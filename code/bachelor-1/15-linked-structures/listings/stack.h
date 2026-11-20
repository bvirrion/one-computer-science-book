// stack.h: the abstract type "stack of int", two implementations behind it.
#ifndef STACK_H
#define STACK_H
#include <stdbool.h>

typedef struct stack stack;

stack *stack_new(void);
void stack_free(stack *s);
bool stack_empty(const stack *s);
void stack_push(stack *s, int x);
int stack_pop(stack *s);        // precondition: not empty
int stack_top(const stack *s);  // precondition: not empty
const char *stack_kind(void);   // which implementation
#endif
