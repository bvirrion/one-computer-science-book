// binom_count.c: Pascal's rule, one call per node of the tree of activations.
#include "binom_count.h"

long binom_counted(int n, int k, long *calls)
{
    ++*calls;
    if (k == 0 || k == n)
        return 1;
    return binom_counted(n - 1, k - 1, calls) + binom_counted(n - 1, k, calls);
}
