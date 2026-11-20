// test-with: ../listings/ratio.c
// The tests of the chapter's ratio module (the same checks as listings/ratio_test.c).
#include "check.h"
#include "ratio.h"

static int is(const struct ratio *r, long num, long den)
{
    return r != NULL && ratio_num(r) == num && ratio_den(r) == den;
}

int main(void)
{
    struct ratio *a = ratio_new(6, -8), *b = ratio_new(1, 6), *z = ratio_new(0, 5);
    struct ratio *s = ratio_add(a, b), *p = ratio_mul(a, b);
    CHECK(is(a, -3, 4) && is(b, 1, 6) && is(z, 0, 1));
    CHECK(is(s, -7, 12) && is(p, -1, 8));
    CHECK(ratio_new(1, 0) == NULL);
    CHECK(ratio_cmp(a, b) < 0 && ratio_cmp(b, a) > 0 && ratio_cmp(a, a) == 0);
    ratio_free(a);
    ratio_free(b);
    ratio_free(z);
    ratio_free(s);
    ratio_free(p);
    return CHECK_REPORT();
}
