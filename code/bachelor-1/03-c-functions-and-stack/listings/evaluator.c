// evaluator.c: three mutually recursive functions, one per rule of the grammar
//   expr   = term { "+" term }      term = factor { "*" factor }
//   factor = digit | "(" expr ")"
#include "evaluator.h"

static const char *p;                   // the next character to read
static int good;

static long expr(void);

static long factor(void)
{
    if (*p >= '0' && *p <= '9')
        return *p++ - '0';
    if (*p == '(') {
        p++;
        long v = expr();                 // factor calls expr: mutual recursion
        if (*p == ')')
            p++;
        else
            good = 0;
        return v;
    }
    good = 0;
    return 0;
}

static long term(void)
{
    long v = factor();
    while (*p == '*') {
        p++;
        v *= factor();
    }
    return v;
}

static long expr(void)
{
    long v = term();
    while (*p == '+') {
        p++;
        v += term();
    }
    return v;
}

long evaluate(const char *text, int *ok)
{
    p = text;
    good = 1;
    long v = expr();
    *ok = good && *p == '\0';
    return *ok ? v : 0;
}
