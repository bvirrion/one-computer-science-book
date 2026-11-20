/* andor.c: run a line of commands joined by && and || (exercise 10). */
#include <string.h>

/* argv: the words of the line, ending with NULL; the words "&&" and "||" are overwritten.
   run: runs one command, returns its exit status. Returns the status of the last command run. */
int run_list(char **argv, int (*run)(char **))
{
    int status = 0;
    int skip = 0;                                 /* this command is not to be run */
    char **start = argv;
    for (char **w = argv;; w++) {
        int end = *w == NULL;
        int and = !end && strcmp(*w, "&&") == 0, or = !end && strcmp(*w, "||") == 0;
        if (!end && !and && !or)
            continue;
        *w = NULL;                                /* cut the command out of the line */
        if (!skip && start != w)
            status = run(start);
        if (end)
            return status;
        skip = and ? status != 0 : status == 0;   /* a && b: b only after a success */
        start = w + 1;
    }
}
