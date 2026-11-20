// uninit.c: a total that nobody set to zero.
#include <stdio.h>

int main(void)
{
    int marks[4] = {12, 15, 9, 14};
    int total;
    for (int i = 0; i < 4; i++)
        total += marks[i];
    printf("total %d\n", total);
    return 0;
}
