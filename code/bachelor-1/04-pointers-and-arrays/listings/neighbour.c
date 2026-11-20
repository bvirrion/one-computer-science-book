// neighbour.c: one write too many changes another array.
// capture: cflags=-O0
#include <stdio.h>

int main(void)
{
    int marks[4] = {12, 15, 9, 14};
    int bonus[4] = {1, 1, 1, 1};
    for (int i = 0; i <= 4; i++)         // one turn too many: i = 4 is outside marks
        marks[i] = 0;
    printf("bonus: %d %d %d %d\n", bonus[0], bonus[1], bonus[2], bonus[3]);
    return 0;
}
