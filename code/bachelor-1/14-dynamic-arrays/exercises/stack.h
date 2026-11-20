// stack.h: the abstract type "stack of int", built on the dynamic array.
#ifndef STACK_H
#define STACK_H
#include <stdbool.h>

typedef struct stack stack;

stack *stack_new(void);         // constructor
void stack_free(stack *s);
bool stack_empty(const stack *s);  // accessors
int stack_top(const stack *s);     // precondition: not empty
void stack_push(stack *s, int x);  // transformers
int stack_pop(stack *s);           // precondition: not empty
#endif
