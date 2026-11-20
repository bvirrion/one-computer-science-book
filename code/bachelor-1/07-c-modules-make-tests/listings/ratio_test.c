// test-with: ratio.c
// ratio_test.c: unit tests of the ratio module.
// capture: with=ratio.c
#include "check.h"
#include "ratio.h"

static int is(const struct ratio *r, long num, long den)
{
    return r != NULL && ratio_num(r) == num && ratio_den(r) == den;
}

int main(void)
{
    struct ratio *r[8];
    r[0] = ratio_new(6, -8);
    CHECK(is(r[0], -3, 4));                                // sign moved to the numerator
    r[1] = ratio_new(0, 5);
    CHECK(is(r[1], 0, 1));                                 // zero has one form
    CHECK(ratio_new(1, 0) == NULL);                        // the boundary of the domain
    r[2] = ratio_new(1, 6);
    r[3] = ratio_add(r[0], r[2]);
    CHECK(is(r[3], -7, 12));
    r[4] = ratio_mul(r[0], r[2]);
    CHECK(is(r[4], -1, 8));
    r[5] = ratio_new(-1, -2);
    CHECK(is(r[5], 1, 2));
    CHECK(ratio_cmp(r[0], r[2]) < 0 && ratio_cmp(r[2], r[0]) > 0);
    r[6] = ratio_new(2, 12);
    CHECK(ratio_cmp(r[2], r[6]) == 0);                     // equal values, different inputs
    r[7] = ratio_add(r[0], r[0]);
    CHECK(is(r[7], -3, 2));
    for (int i = 0; i < 8; i++)
        ratio_free(r[i]);
    return CHECK_REPORT();
}
