// exo_steps.c: the number of steps from n down to zero, by twos.
#include <stdio.h>

int steps(int n)
{
    if (n == 0)
        return 0;
    return 1 + steps(n - 2);
}

int main(void)
{
    printf("steps(10) = %d\n", steps(10));
    printf("steps(7)  = %d\n", steps(7));
    return 0;
}
