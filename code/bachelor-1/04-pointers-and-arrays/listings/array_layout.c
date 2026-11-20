// array_layout.c: the elements of an array, one after the other.
#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    for (int i = 0; i <= 5; i++)         // i = 5: the one-past-the-end pointer, never dereferenced
        printf("a + %d is %2td bytes after a\n", i, (char *)(a + i) - (char *)a);
    printf("a[3] = %d, *(a + 3) = %d\n", a[3], *(a + 3));
    int *p = &a[1], *q = &a[4];
    printf("q - p = %td elements\n", q - p);
    printf("sizeof a = %zu bytes, %zu elements\n", sizeof a, sizeof a / sizeof a[0]);
    return 0;
}
