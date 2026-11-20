// average.c: the average mark comes out as a whole number.
#include <stdio.h>

int main(void)
{
    int marks[] = {12, 15, 9, 14};
    int sum = 0;
    for (int i = 0; i < 4; i++)
        sum += marks[i];
    double average = sum / 4;
    printf("average = %.2f\n", average);
    return 0;
}
