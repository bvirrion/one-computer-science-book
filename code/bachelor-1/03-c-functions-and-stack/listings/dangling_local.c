// dangling_local.c: returning the address of a local variable.
#include <stdio.h>

int *make_counter(void)
{
    int count = 42;
    return &count;                       // count dies when the function returns
}

int main(void)
{
    int *c = make_counter();
    printf("the returned address is %p\n", (void *)c);
    return 0;
}
