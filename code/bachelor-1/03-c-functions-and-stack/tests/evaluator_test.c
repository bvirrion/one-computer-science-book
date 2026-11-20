// test-with: ../listings/evaluator.c
#include <assert.h>
#include <stdio.h>
#include "evaluator.h"

static long ok_value(const char *s)
{
    int ok;
    long v = evaluate(s, &ok);
    assert(ok);
    return v;
}

static void bad(const char *s)
{
    int ok;
    evaluate(s, &ok);
    assert(!ok);
}

int main(void)
{
    assert(ok_value("7") == 7);
    assert(ok_value("1+2*3") == 7);
    assert(ok_value("(1+2)*3") == 9);
    assert(ok_value("2*(3+(4*5))") == 46);
    assert(ok_value("((((9))))") == 9);
    assert(ok_value("1+1+1+1*0") == 3);
    bad("");
    bad("2*(3+");
    bad("1+");
    bad("(1))");
    bad("12");
    puts("evaluator_test: ok");
    return 0;
}
