/* pipeline_lib.c: stage i reads from pipe i - 1 and writes into pipe i. */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

#include "pipeline.h"

int run_pipeline(char **const stages[], int k)   /* returns the last stage's status */
{
    int prev = -1;                               /* read end of the previous pipe */
    pid_t last = -1;
    for (int i = 0; i < k; i++) {
        int fd[2] = {-1, -1};
        if (i < k - 1 && pipe(fd) != 0)
            return 1;
        pid_t r = fork();
        if (r == 0) {
            if (prev != -1) {                    /* standard input from the previous stage */
                dup2(prev, 0);
                close(prev);
            }
            if (fd[1] != -1) {                   /* standard output into the next pipe */
                dup2(fd[1], 1);
                close(fd[1]);
                close(fd[0]);
            }
            execvp(stages[i][0], stages[i]);
            perror(stages[i][0]);
            _exit(127);
        }
        if (prev != -1)
            close(prev);                         /* the parent keeps no end it does not use */
        if (fd[1] != -1)
            close(fd[1]);
        prev = fd[0];
        last = r;
    }
    int status = 0, s;
    pid_t w;
    while ((w = wait(&s)) > 0)                   /* every stage, in any order */
        if (w == last)
            status = WIFEXITED(s) ? WEXITSTATUS(s) : 128 + WTERMSIG(s);
    return status;
}
