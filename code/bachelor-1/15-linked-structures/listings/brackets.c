// brackets.c: checking brackets with a stack, whichever implementation is linked.
// capture: with=stack_list.c
#include "stack.h"
#include <stdio.h>

// returns -1 if balanced, else the position of the first error
static int check(const char *s) {
    stack *st = stack_new();
    int i = 0, error = -1;
    for (; s[i] != '\0' && error < 0; i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') stack_push(st, c);
        else if (c == ')' || c == ']' || c == '}') {
            char open = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (stack_empty(st) || stack_pop(st) != open) error = i;
        }
    }
    if (error < 0 && !stack_empty(st)) error = i;  // unclosed at the end
    stack_free(st);
    return error;
}

int main(void) {
    printf("stack on %s\n", stack_kind());
    const char *tests[] = {"a[i] = f(b[j], {c})", "(a + b]", "((x)", "x)"};
    for (int t = 0; t < 4; t++) {
        int e = check(tests[t]);
        if (e < 0) printf("%-20s balanced\n", tests[t]);
        else printf("%-20s error at position %d\n", tests[t], e);
    }
    return 0;
}
