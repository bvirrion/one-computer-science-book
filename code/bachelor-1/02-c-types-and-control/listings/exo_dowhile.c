// exo_dowhile.c: a do-while loop and a while loop on the same condition.
#include <stdio.h>

int main(void)
{
    int n = 20, steps = 0;
    do {
        n -= 7;
        steps++;
    } while (n > 0);
    int m = -1, turns = 0;
    while (m > 0) {
        m -= 7;
        turns++;
    }
    printf("n = %d after %d steps; m = %d after %d turns\n", n, steps, m, turns);
    return 0;
}
