// assert_demo.c: an assertion states what must be true; a failed one stops the program.
#include <assert.h>
#include <stdio.h>

double mean(const double *x, int n)
{
    assert(n > 0);                          // a caller's error, not a run-time condition
    double s = 0.0;
    for (int i = 0; i < n; i++)
        s += x[i];
    return s / n;
}

int main(void)
{
    double rain[3] = {1.0, 2.5, 0.0};
    printf("mean of 3: %.2f\n", mean(rain, 3));
    printf("mean of 0: %.2f\n", mean(rain, 0));
    return 0;
}
