// stack.h: a stack of int, as an opaque type (exercise 7).
#ifndef STACK_H
#define STACK_H
#include <stddef.h>

struct stack;

struct stack *stack_new(void);                      // NULL if out of memory; free with stack_free
void stack_free(struct stack *s);
int stack_push(struct stack *s, int v);              // 0, or -1 if out of memory
int stack_pop(struct stack *s, int *v);              // 0, or -1 if the stack is empty
size_t stack_size(const struct stack *s);

#endif
