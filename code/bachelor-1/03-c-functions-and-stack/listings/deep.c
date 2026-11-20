// deep.c: go down until the stack runs out, printing each depth reached.
#include <stdint.h>
#include <stdio.h>

static uintptr_t top;

void dive(long depth)
{
    volatile char pad[1000];             // make each frame about 1 KiB
    pad[0] = (char)depth;
    if (depth == 0)
        top = (uintptr_t)pad;
    if (depth == 1)
        printf("frame size: %lu bytes\n", (unsigned long)(top - (uintptr_t)pad));
    printf("depth %ld\n", depth);
    fflush(stdout);                      // print now: the crash would lose the buffer
    dive(depth + 1);
    pad[1] = 0;                          // work after the call: no tail call
}

int main(void)
{
    dive(0);
    return 0;
}
