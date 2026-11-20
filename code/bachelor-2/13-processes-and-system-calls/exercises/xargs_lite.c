/* xargs_lite.c: read words from standard input; run the command on them, at most n at a time
   (exercise 7). Usage: xargs_lite n command [argument...] */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAXWORDS 1024

static int run(char **argv)
{
    fflush(stdout);
    pid_t r = fork();
    if (r == 0) {
        execvp(argv[0], argv);
        perror("xargs_lite: exec");
        _exit(127);
    }
    int status;
    if (r < 0 || waitpid(r, &status, 0) < 0)
        return 1;
    return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}

int main(int argc, char **argv)
{
    if (argc < 3 || atoi(argv[1]) < 1 || argc - 2 + atoi(argv[1]) > MAXWORDS)
        return 2;
    int n = atoi(argv[1]), fixed = argc - 2, worst = 0;
    char *cmd[MAXWORDS + 1], word[256];
    for (int k = 0; k < fixed; k++)
        cmd[k] = argv[k + 2];                     /* the command and its own arguments */
    int used = 0;
    for (;;) {
        int got = scanf("%255s", word) == 1;
        if (got)
            cmd[fixed + used++] = strdup(word);
        if (used > 0 && (used == n || !got)) {    /* a full batch, or the last one */
            cmd[fixed + used] = NULL;
            int s = run(cmd);
            worst = s > worst ? s : worst;
            for (int k = 0; k < used; k++)
                free(cmd[fixed + k]);
            used = 0;
        }
        if (!got)
            return worst;
    }
}
