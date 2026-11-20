// exo_feof.c: summing the numbers of standard input, the classic wrong way.
// capture: cflags=-O2 -Wall -Wno-unused-result
#include <stdio.h>

int main(void)
{
    int v, total = 0, count = 0;
    while (!feof(stdin)) {
        scanf("%d", &v);
        total += v;
        count++;
    }
    printf("%d numbers, total %d\n", count, total);
    return 0;
}
