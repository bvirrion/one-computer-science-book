// countdown.c: a countdown to zero with an unsigned counter (it never ends).
#include <stdio.h>

int main(void)
{
    int guard = 0;                       // stops the demonstration after 6 turns
    for (unsigned i = 3; i >= 0; i--) {
        printf("%u\n", i);
        if (++guard == 6) {
            puts("... and so on, forever");
            break;
        }
    }
    return 0;
}
