// exo_switch.c: a switch whose cases fall through on purpose.
#include <stdio.h>

int main(void)
{
    for (int level = 1; level <= 3; level++) {
        int score = 0;
        switch (level) {
        case 1:
            score += 100;
            /* fall through */
        case 2:
            score += 10;
            /* fall through */
        case 3:
            score += 1;
        }
        printf("level %d: %d\n", level, score);
    }
    return 0;
}
