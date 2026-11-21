/* wait_status.c: four children end four ways; the parent reads how from the status. */
#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static void report(const char *what, int status)
{
    if (WIFEXITED(status))
        printf("%-22s exited with status %d\n", what, WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
        printf("%-22s killed by signal %d (%s)\n", what, WTERMSIG(status),
               strsignal(WTERMSIG(status)));
}

int main(void)
{
    const char *what[] = {"return 0 from main", "exit(3)", "raise(SIGTERM)", "exit(300)"};
    for (int k = 0; k < 4; k++) {
        fflush(stdout);                              /* or each child prints the lines again */
        pid_t r = fork();
        if (r == 0) {
            if (k == 0) return 0;
            if (k == 1) exit(3);
            if (k == 2) raise(SIGTERM);
            exit(300);                               /* only the low 8 bits survive */
        }
        int status;
        waitpid(r, &status, 0);
        report(what[k], status);
    }
    return 0;
}
