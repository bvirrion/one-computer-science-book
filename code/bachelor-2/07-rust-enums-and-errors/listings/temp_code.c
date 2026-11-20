/* temp_code.c: a temperature field read in tenths of a degree; -1 means "unreadable". */
#include <stdio.h>
#include <stdlib.h>

int temp_tenths(const char *field)
{
    char *end;
    double t = strtod(field, &end);
    if (end == field || *end != '\0')
        return -1;                          /* no number, or garbage after it */
    return (int)(t * 10 + (t < 0 ? -0.5 : 0.5));
}

int main(void)
{
    const char *fields[] = {"4.3", "", "-0.1", "n/a", "-12.5"};
    for (int i = 0; i < 5; i++) {
        int t = temp_tenths(fields[i]);
        printf("%-6s -> %4d  %s\n", fields[i], t, t == -1 ? "unreadable?" : "");
    }
    return 0;
}
