/* sigpipe.c: writing into a pipe that nobody reads. */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static void writer(int ignore)
{
    int fd[2];
    if (pipe(fd) != 0) _exit(1);
    close(fd[0]);                                /* no reader left */
    if (ignore)
        signal(SIGPIPE, SIG_IGN);
    ssize_t n = write(fd[1], "x", 1);
    printf("write returned %zd, errno %s\n", n, n < 0 ? strerror(errno) : "-");
    fflush(stdout);
    _exit(0);
}

int main(void)
{
    for (int ignore = 0; ignore <= 1; ignore++) {
        fflush(stdout);
        pid_t r = fork();
        if (r == 0)
            writer(ignore);
        int s;
        waitpid(r, &s, 0);
        if (WIFSIGNALED(s))
            printf("SIGPIPE %s: the writer was killed by signal %d\n",
                   ignore ? "ignored" : "default", WTERMSIG(s));
        else
            printf("SIGPIPE %s: the writer went on and exited normally\n",
                   ignore ? "ignored" : "default");
    }
    return 0;
}
