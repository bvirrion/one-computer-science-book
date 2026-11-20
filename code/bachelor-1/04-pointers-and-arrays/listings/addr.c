// addr.c: a variable, its address, and a pointer that holds it.
#include <stdio.h>

int main(void)
{
    int n = 5;
    int *p = &n;                         // p holds the address of n
    printf("n = %d, *p = %d\n", n, *p);
    printf("p == &n: %d\n", p == &n);
    *p = 7;                              // writes 7 at that address: into n
    printf("after *p = 7: n = %d\n", n);
    printf("sizeof n = %zu, sizeof p = %zu\n", sizeof n, sizeof p);
    int *nowhere = NULL;
    printf("nowhere == NULL: %d\n", nowhere == NULL);
    return 0;
}
