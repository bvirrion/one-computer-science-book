// exo_strcat.c: building a greeting.
#include <stdio.h>
#include <string.h>

int main(void)
{
    char greeting[16] = "Hello, ";
    strcat(greeting, "Christabelle");
    strcat(greeting, "!");
    printf("%s\n", greeting);
    return 0;
}
