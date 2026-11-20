// test-with: ../exercises/stack.c
#include "check.h"
#include "../exercises/stack.h"

int main(void)
{
    struct stack *s = stack_new();
    int v = 0;
    CHECK(s != NULL && stack_size(s) == 0);
    CHECK(stack_pop(s, &v) == -1);                       // empty: the boundary
    for (int i = 0; i < 100; i++)
        CHECK(stack_push(s, i) == 0);
    CHECK(stack_size(s) == 100);
    int ok = 1;
    for (int i = 99; i >= 0; i--)
        ok = ok && stack_pop(s, &v) == 0 && v == i;      // last in, first out
    CHECK(ok);
    CHECK(stack_pop(s, &v) == -1 && stack_size(s) == 0);
    stack_free(s);
    stack_free(NULL);
    return CHECK_REPORT();
}
