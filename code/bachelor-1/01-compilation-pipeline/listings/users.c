// users.c: one file of the program; uses max_users.
#include <stdio.h>
#include "limits_bad.h"

void admin_report(void);

int main(void)
{
    printf("max users: %d\n", max_users);
    admin_report();
    return 0;
}
