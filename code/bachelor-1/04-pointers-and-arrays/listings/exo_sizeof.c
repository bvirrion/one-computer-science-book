// exo_sizeof.c: the length of an array, computed in two places.
#include <stdio.h>

size_t length(const double values[])
{
    return sizeof values / sizeof values[0];
}

int main(void)
{
    double values[10] = {0};
    printf("in main: %zu, in length: %zu\n", sizeof values / sizeof values[0], length(values));
    return 0;
}
