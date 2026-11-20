// counter_static.c: a local that survives the call, and one that does not.
#include <stdio.h>

void visit(void)
{
    static int visits = 0;               // created once, before main
    int fresh = 0;                       // created at each call
    visits++;
    fresh++;
    printf("visits = %d, fresh = %d\n", visits, fresh);
}

int main(void)
{
    visit();
    visit();
    visit();
    return 0;
}
