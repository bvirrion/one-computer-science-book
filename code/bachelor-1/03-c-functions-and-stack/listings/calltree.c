// calltree.c: the tree of activations of binom(4, 2), one line per call.
#include <stdio.h>

static int calls = 0;

long binom(int n, int k, int depth)
{
    calls++;
    printf("%*sbinom(%d, %d)\n", 2 * depth, "", n, k);
    if (k == 0 || k == n)
        return 1;                                   // a leaf of the tree
    return binom(n - 1, k - 1, depth + 1) + binom(n - 1, k, depth + 1);
}

int main(void)
{
    long r = binom(4, 2, 0);
    printf("result %ld after %d calls\n", r, calls);
    return 0;
}
