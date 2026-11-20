// exo_parity.c: is_even and is_odd, with a trace of each call.
#include <stdbool.h>
#include <stdio.h>

bool is_odd(int n);

bool is_even(int n)
{
    printf("is_even(%d) ", n);
    return n == 0 ? true : is_odd(n - 1);
}

bool is_odd(int n)
{
    printf("is_odd(%d) ", n);
    return n == 0 ? false : is_even(n - 1);
}

int main(void)
{
    bool r = is_odd(7);
    printf("\nresult %d\n", r);
    return 0;
}
