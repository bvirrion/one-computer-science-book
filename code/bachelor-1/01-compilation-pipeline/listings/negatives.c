// negatives.c: count the negative readings (it always finds none).
#include <stdio.h>

int main(void)
{
    unsigned int readings[] = {3, -2, 7, -5, 0};
    int count = 0;
    for (int i = 0; i < 5; i++)
        if (readings[i] < 0)
            count++;
    printf("negative readings: %d\n", count);
    return 0;
}
