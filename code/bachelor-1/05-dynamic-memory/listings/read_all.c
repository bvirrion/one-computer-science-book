// read_all.c: read whole numbers until the end of the input, however many there are.
// capture: with=intvec.c
#include <stdio.h>
#include "intvec.h"

int main(void)
{
    struct intvec v;
    intvec_init(&v);
    int x;
    while (scanf("%d", &x) == 1) {
        size_t old_cap = v.cap;
        if (intvec_push(&v, x) != 0) {
            printf("out of memory after %zu numbers\n", v.len);
            break;
        }
        if (v.cap != old_cap)
            printf("capacity %zu -> %zu when number %zu arrives\n", old_cap, v.cap, v.len);
    }
    long sum = 0;
    for (size_t i = 0; i < v.len; i++)
        sum += v.data[i];
    printf("%zu numbers, sum %ld, %ld element copies\n", v.len, sum, v.copies);
    intvec_free(&v);
    return 0;
}
