// exo_loop.c: the average of the monthly rainfall.
// built with -O0 -g -fsanitize=address (see exo_loop_asan.sh)
#include <stdio.h>

double rain[12] = {48.0, 39.5, 41.0, 52.5, 60.0, 45.5, 30.0, 35.5, 50.0, 66.0, 71.5, 58.0};

int main(void)
{
    int n = 12;
    double total = 0;
    for (int i = 0; i <= n; i++)
        total += rain[i];
    printf("average %.2f mm\n", total / n);
    return 0;
}
