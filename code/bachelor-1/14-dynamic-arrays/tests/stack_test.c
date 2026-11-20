// test-with: ../exercises/stack.c ../listings/vec.c
// The stack: last in, first out, and its use to check brackets.
#include "../exercises/stack.h"
#include <assert.h>
#include <stdio.h>

static int balanced(const char *s) {
    stack *st = stack_new();
    int ok = 1;
    for (; *s && ok; s++) {
        if (*s == '(' || *s == '[') stack_push(st, *s);
        else if (*s == ')' || *s == ']') {
            int want = *s == ')' ? '(' : '[';
            ok = !stack_empty(st) && stack_pop(st) == want;
        }
    }
    ok = ok && stack_empty(st);
    stack_free(st);
    return ok;
}

int main(void) {
    stack *s = stack_new();
    assert(stack_empty(s));
    for (int i = 0; i < 1000; i++) stack_push(s, i);
    assert(stack_top(s) == 999);
    for (int i = 999; i >= 0; i--) assert(stack_pop(s) == i);
    assert(stack_empty(s));
    stack_free(s);
    assert(balanced("([()[]])") && !balanced("([)]") && !balanced("((") && balanced(""));
    puts("stack: ok");
    return 0;
}
