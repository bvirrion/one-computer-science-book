/* capture_cmd.c: run a command with a string as its standard input; return what it prints
   (exercise 9). */
#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

char *capture(char *const argv[], const char *input, int *status)
{
    int to[2], from[2];
    if (pipe(to) != 0 || pipe(from) != 0)
        return NULL;
    pid_t cmd = fork();
    if (cmd == 0) {                               /* stdin from to, stdout into from */
        dup2(to[0], 0);
        dup2(from[1], 1);
        close(to[0]), close(to[1]), close(from[0]), close(from[1]);
        execvp(argv[0], argv);
        _exit(127);
    }
    pid_t feeder = fork();
    if (feeder == 0) {                            /* a second child writes the input */
        close(to[0]), close(from[0]), close(from[1]);
        size_t n = strlen(input);
        _exit(write(to[1], input, n) == (ssize_t)n ? 0 : 1);
    }
    close(to[0]), close(to[1]), close(from[1]);   /* or the command never sees end of file */
    size_t len = 0, cap = 256;
    char *out = malloc(cap);
    ssize_t n;
    while (out && (n = read(from[0], out + len, cap - len - 1)) > 0)
        if ((len += n) + 1 == cap)
            out = realloc(out, cap *= 2);
    close(from[0]);
    waitpid(feeder, NULL, 0);
    int s = 0;
    waitpid(cmd, &s, 0);
    if (status)
        *status = WIFEXITED(s) ? WEXITSTATUS(s) : 128 + WTERMSIG(s);
    if (out)
        out[len] = '\0';
    return out;
}
