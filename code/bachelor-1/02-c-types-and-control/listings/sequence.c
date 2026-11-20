// sequence.c: two side effects on one variable, with no order between them.
#include <stdio.h>

int main(void)
{
    int i = 1;
    i = i++ + 1;                         // undefined behaviour
    printf("i = %d\n", i);
    return 0;
}
