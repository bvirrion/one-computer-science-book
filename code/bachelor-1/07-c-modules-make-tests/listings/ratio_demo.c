// ratio_demo.c: a user of the module, which knows only ratio.h.
// capture: with=ratio.c
#include <stdio.h>
#include "ratio.h"

int main(void)
{
    struct ratio *a = ratio_new(6, -8), *b = ratio_new(1, 6);
    struct ratio *s = ratio_add(a, b), *p = ratio_mul(a, b);
    printf("a = %ld/%ld, b = %ld/%ld\n", ratio_num(a), ratio_den(a), ratio_num(b), ratio_den(b));
    printf("a + b = %ld/%ld, a * b = %ld/%ld\n", ratio_num(s), ratio_den(s), ratio_num(p), ratio_den(p));
    printf("compare(a, b) = %d, ratio_new(1, 0) = %p\n", ratio_cmp(a, b), (void *)ratio_new(1, 0));
    ratio_free(a);
    ratio_free(b);
    ratio_free(s);
    ratio_free(p);
    return 0;
}
