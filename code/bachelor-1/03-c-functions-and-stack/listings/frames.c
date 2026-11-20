// frames.c: where the local variable of each call lives.
// capture: cflags=-O0
#include <stdint.h>
#include <stdio.h>

static uintptr_t first;

void descend(int depth)
{
    int local = depth;
    uintptr_t here = (uintptr_t)&local;
    if (depth == 0)
        first = here;
    printf("depth %d: local at first - %3lu bytes\n", depth, (unsigned long)(first - here));
    if (depth < 4)
        descend(depth + 1);
}

int main(void)
{
    descend(0);
    return 0;
}
