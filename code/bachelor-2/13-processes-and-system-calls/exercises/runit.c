/* runit.c: run the command given on the command line; exit with its status, as a shell would
   report it (exercise 3). */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: runit command [argument...]\n");
        return 2;
    }
    pid_t r = fork();
    if (r < 0) {
        perror("runit: fork");
        return 1;
    }
    if (r == 0) {
        execvp(argv[1], argv + 1);                /* argv + 1 ends with argv's null pointer */
        perror("runit: exec");
        _exit(127);
    }
    int status;
    if (waitpid(r, &status, 0) < 0)
        return 1;
    if (WIFEXITED(status))
        return WEXITSTATUS(status);
    return 128 + WTERMSIG(status);                /* killed by signal n: 128 + n */
}
