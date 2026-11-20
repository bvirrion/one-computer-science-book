// even_odd.c: two functions that call each other.
#include <stdbool.h>
#include <stdio.h>

bool is_odd(unsigned n);                 // declared first: is_even calls it

bool is_even(unsigned n)
{
    return n == 0 ? true : is_odd(n - 1);
}

bool is_odd(unsigned n)
{
    return n == 0 ? false : is_even(n - 1);
}

int main(void)
{
    for (unsigned n = 0; n <= 3; n++)
        printf("%u: even %d, odd %d\n", n, is_even(n), is_odd(n));
    return 0;
}
