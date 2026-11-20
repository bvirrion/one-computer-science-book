// parity_deep.c: mutual recursion ten million calls deep.
#include <stdbool.h>
#include <stdio.h>

bool is_odd(long n);

bool is_even(long n)
{
    return n == 0 ? true : is_odd(n - 1);
}

bool is_odd(long n)
{
    return n == 0 ? false : is_even(n - 1);
}

int main(void)
{
    printf("is_even(10000000) = %d\n", is_even(10000000));
    return 0;
}
