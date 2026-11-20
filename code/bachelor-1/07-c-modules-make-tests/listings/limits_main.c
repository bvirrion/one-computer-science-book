// limits_main.c: prints a limit set in config.h.
#include <stdio.h>
#include "config.h"

int main(void)
{
    printf("a member may borrow %d books\n", MAX_LOANS);
    return 0;
}
