// calls.c: a static local and an automatic local across three calls.
#include <stdio.h>

void tick(void)
{
    static int kept = 0;
    int fresh = 0;
    kept++;
    fresh++;
    printf("kept = %d, fresh = %d\n", kept, fresh);
}

int main(void)
{
    tick();
    tick();
    tick();
    return 0;
}
