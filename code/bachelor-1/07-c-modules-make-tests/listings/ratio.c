// ratio.c: the implementation, free to change as long as ratio.h is honoured.
#include <stdlib.h>
#include "ratio.h"

struct ratio {
    long num, den;                          // lowest terms, den > 0
};

static long gcd(long a, long b)             // static: invisible outside this file
{
    if (a < 0)
        a = -a;
    while (b != 0) {
        long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

struct ratio *ratio_new(long num, long den)
{
    if (den == 0)
        return NULL;
    struct ratio *r = malloc(sizeof *r);
    if (r == NULL)
        return NULL;
    if (den < 0) {
        num = -num;
        den = -den;
    }
    long g = gcd(num, den);
    r->num = num / g;
    r->den = den / g;
    return r;
}

void ratio_free(struct ratio *r) { free(r); }
long ratio_num(const struct ratio *r) { return r->num; }
long ratio_den(const struct ratio *r) { return r->den; }

struct ratio *ratio_add(const struct ratio *a, const struct ratio *b)
{
    return ratio_new(a->num * b->den + b->num * a->den, a->den * b->den);
}

struct ratio *ratio_mul(const struct ratio *a, const struct ratio *b)
{
    return ratio_new(a->num * b->num, a->den * b->den);
}

int ratio_cmp(const struct ratio *a, const struct ratio *b)
{
    long left = a->num * b->den, right = b->num * a->den;
    return (left > right) - (left < right);
}
