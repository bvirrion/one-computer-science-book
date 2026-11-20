// stack_suite.h: one suite for any implementation of stack.h.
#include "stack.h"
#include <assert.h>
#include <stdio.h>

static int stack_suite(void) {
    stack *s = stack_new();
    assert(stack_empty(s));
    for (int i = 0; i < 10000; i++) stack_push(s, i), assert(stack_top(s) == i);
    for (int i = 9999; i >= 5000; i--) assert(stack_pop(s) == i);
    stack_push(s, -1);
    assert(stack_pop(s) == -1 && stack_top(s) == 4999);
    for (int i = 4999; i >= 0; i--) assert(stack_pop(s) == i);
    assert(stack_empty(s));
    stack_free(s);
    printf("stack on %s: ok\n", stack_kind());
    return 0;
}
