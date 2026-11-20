/* minish_parse.c: cut a line at blanks; the word $? becomes the last exit status. */
#include <stdio.h>
#include <string.h>

#include "minish_parse.h"

int split(char *line, char **argv, int max, int last)
{
    static char status[12];
    int argc = 0;
    for (char *w = strtok(line, " \t\n"); w && argc < max; w = strtok(NULL, " \t\n")) {
        if (strcmp(w, "$?") == 0) {
            snprintf(status, sizeof status, "%d", last);
            w = status;
        }
        argv[argc++] = w;                     /* a pointer into the line itself */
    }
    argv[argc] = NULL;                        /* exec wants a null pointer at the end */
    return argc;
}
