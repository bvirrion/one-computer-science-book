/* minish.c: a minimal shell. Read a line, split it, run it, wait; cd and exit are built in. */
// capture: with=minish_parse.c exit
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "minish_parse.h"

static int run(char **argv)                   /* an external command: its exit status */
{
    pid_t r = fork();
    if (r < 0) {
        perror("minish: fork");
        return 1;
    }
    if (r == 0) {                             /* the child becomes the command */
        execvp(argv[0], argv);
        fprintf(stderr, "minish: %s: command not found\n", argv[0]);
        _exit(127);                           /* never return into the shell's loop */
    }
    int status;
    if (waitpid(r, &status, 0) < 0)
        return 1;
    return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}

static int cd(int argc, char **argv)          /* must run in the shell's own process */
{
    const char *dir = argc > 1 ? argv[1] : getenv("HOME");
    if (dir && chdir(dir) == 0)
        return 0;
    fprintf(stderr, "minish: cd: %s: cannot go there\n", dir ? dir : "(no HOME)");
    return 1;
}

int main(void)
{
    char line[1024], *argv[MAXARGS + 1];
    int last = 0;
    for (;;) {
        printf("minish$ ");
        if (!fgets(line, sizeof line, stdin))
            break;                            /* end of input: leave like exit */
        if (!isatty(0))
            fputs(line, stdout);              /* a script: show the line as if typed */
        fflush(stdout);                       /* before fork: the prompt before the output */
        int argc = split(line, argv, MAXARGS, last);
        if (argc == 0)
            continue;
        if (strcmp(argv[0], "exit") == 0)
            return argc > 1 ? atoi(argv[1]) : last;
        last = strcmp(argv[0], "cd") == 0 ? cd(argc, argv) : run(argv);
    }
    printf("\n");
    return last;
}
