/* cd_dash.c: the built-in cd with `cd -`, back to the previous directory (exercise 9). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int cd_builtin(int argc, char **argv)
{
    static char previous[4096] = "";
    char here[4096];
    if (!getcwd(here, sizeof here))
        return 1;
    const char *dir = argc > 1 ? argv[1] : getenv("HOME");
    int back = dir && strcmp(dir, "-") == 0;
    if (back && previous[0] == '\0') {
        fprintf(stderr, "cd: no previous directory\n");
        return 1;
    }
    if (back)
        dir = previous;
    if (!dir || chdir(dir) != 0) {
        fprintf(stderr, "cd: %s: cannot go there\n", dir ? dir : "(no HOME)");
        return 1;
    }
    if (back)
        printf("%s\n", previous);                 /* as bash does */
    strcpy(previous, here);                       /* only after a successful change */
    return 0;
}
