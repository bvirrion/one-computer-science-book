// decay.c: inside a function, an array parameter is a pointer.
#include <stdio.h>

long sum(int a[], size_t n)              // the same as: long sum(int *a, size_t n)
{
    printf("in sum:  sizeof a = %zu\n", sizeof a);
    long s = 0;
    for (size_t i = 0; i < n; i++)
        s += a[i];
    return s;
}

int main(void)
{
    int days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    printf("in main: sizeof days = %zu\n", sizeof days);
    printf("sum = %ld\n", sum(days, sizeof days / sizeof days[0]));
    return 0;
}
