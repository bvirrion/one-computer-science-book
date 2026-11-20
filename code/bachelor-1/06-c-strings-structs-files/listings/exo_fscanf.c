// exo_fscanf.c: what does scanf return?
#include <stdio.h>

int main(void)
{
    int day, rain;
    int r;
    while ((r = scanf("%d %d", &day, &rain)) == 2)
        printf("day %d: %d\n", day, rain);
    printf("last return value: %d\n", r);
    return 0;
}
