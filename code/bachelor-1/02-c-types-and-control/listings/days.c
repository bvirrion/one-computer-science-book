// days.c: a switch that forgets a break.
#include <stdio.h>

int days_in(int month)
{
    int days = 0;
    switch (month) {
    case 2:
        days = 28;
        break;
    case 4: case 6: case 9: case 11:
        days = 30;
    default:
        days = 31;
    }
    return days;
}

int main(void)
{
    printf("February %d, April %d, May %d\n", days_in(2), days_in(4), days_in(5));
    return 0;
}
