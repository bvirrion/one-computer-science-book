/* exec_demo.c: the same process runs another program, with an argument vector and an environment. */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    printf("exec_demo: three programs follow\n");
    fflush(stdout);                                  /* or the line dies with the old image */
    pid_t r = fork();
    if (r == 0) {
        char *argv[] = {"echo", "two words", "three", NULL};
        execvp("echo", argv);                        /* searched for in the PATH */
        perror("execvp");                            /* reached only if exec failed */
        _exit(127);
    }
    waitpid(r, NULL, 0);
    if (fork() == 0) {
        char *argv[] = {"env", NULL};
        char *envp[] = {"LIBRARY=town", "OPENS=9", NULL};
        execve("/usr/bin/env", argv, envp);          /* a full path, and a new environment */
        perror("execve");
        _exit(127);
    }
    wait(NULL);
    execlp("printf", "printf", "%s+%s\n", "a", "b", (char *)NULL);   /* this process itself */
    printf("this line is never printed\n");
    return 1;
}
