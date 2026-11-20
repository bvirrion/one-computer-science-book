// safe_copy.c: snprintf never writes more than the size it is given, and says how much it wanted.
#include <stdio.h>

int main(void)
{
    char name[10];
    const char *names[] = {"Ann", "Wilhelmina", "Christabelle"};
    for (int i = 0; i < 3; i++) {
        int needed = snprintf(name, sizeof name, "%s", names[i]);
        if (needed >= (int)sizeof name)
            printf("\"%s\" truncated: kept \"%s\", needed %d + 1 bytes\n", names[i], name, needed);
        else
            printf("\"%s\" fits\n", name);
    }
    return 0;
}
