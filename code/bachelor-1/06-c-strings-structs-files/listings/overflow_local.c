// overflow_local.c: the same copy into a plain local array.
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[10];
    strcpy(name, "Christabelle");
    printf("%s\n", name);
    return 0;
}
