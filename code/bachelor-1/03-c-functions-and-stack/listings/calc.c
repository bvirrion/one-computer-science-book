// calc.c: try the evaluator on four expressions.
// capture: with=evaluator.c
#include <stdio.h>
#include "evaluator.h"

int main(void)
{
    const char *tests[] = {"1+2*3", "(1+2)*3", "2*(3+(4*5))", "2*(3+"};
    for (int i = 0; i < 4; i++) {
        int ok;
        long v = evaluate(tests[i], &ok);
        if (ok)
            printf("%-12s = %ld\n", tests[i], v);
        else
            printf("%-12s : syntax error\n", tests[i]);
    }
    return 0;
}
