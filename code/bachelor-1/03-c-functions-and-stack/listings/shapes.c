// shapes.c: calls and greatest depth for three shapes of recursion.
#include <stdio.h>

static long calls;
static int deepest;

static void enter(int depth)
{
    calls++;
    if (depth > deepest)
        deepest = depth;
}

long count_down(int n, int depth)                 // linear: one call inside
{
    enter(depth);
    return n == 0 ? 0 : 1 + count_down(n - 1, depth + 1);
}

long fib(int n, int depth)                        // binary: two calls inside
{
    enter(depth);
    return n < 2 ? n : fib(n - 1, depth + 1) + fib(n - 2, depth + 1);
}

long hanoi(int n, int depth)                      // binary, both of size n - 1
{
    enter(depth);
    return n == 0 ? 0 : hanoi(n - 1, depth + 1) + 1 + hanoi(n - 1, depth + 1);
}

int main(void)
{
    long (*shape[3])(int, int) = {count_down, fib, hanoi};
    const char *name[3] = {"count_down", "fib", "hanoi"};
    printf("%-10s %3s %8s %6s\n", "shape", "n", "calls", "depth");
    for (int s = 0; s < 3; s++)
        for (int n = 5; n <= 20; n += 5) {
            calls = 0;
            deepest = 0;
            shape[s](n, 1);
            printf("%-10s %3d %8ld %6d\n", name[s], n, calls, deepest);
        }
    return 0;
}
