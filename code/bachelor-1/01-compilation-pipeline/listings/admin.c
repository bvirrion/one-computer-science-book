// admin.c: another file of the program; also uses max_users.
#include <stdio.h>
#include "limits_bad.h"

void admin_report(void)
{
    printf("admin sees max users: %d\n", max_users);
}
