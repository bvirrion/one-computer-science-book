/* rlimit.c -- a resource limit: the child caps its own address space at 64 MiB, then
   allocates 16 MiB blocks until one is refused. It fails cleanly, and the parent goes on. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <unistd.h>

#define MIB (1024L * 1024L)

int main(void) {
    pid_t pid = fork();
    if (pid == 0) {                                      /* the child */
        struct rlimit cap = {64 * MIB, 64 * MIB};       /* soft and hard limit */
        setrlimit(RLIMIT_AS, &cap);
        int blocks = 0;
        for (;;) {
            char *p = malloc(16 * MIB);
            if (p == NULL) break;                        /* refused: the limit is reached */
            memset(p, 1, 16 * MIB);                      /* really use the memory */
            blocks++;
        }
        printf("child: %d blocks of 16 MiB, then malloc returned NULL\n", blocks);
        exit(blocks > 0 ? 0 : 1);
    }
    int status;
    waitpid(pid, &status, 0);
    printf("parent: the child exited with status %d; the parent is unaffected\n",
           WEXITSTATUS(status));
    char *q = malloc(256 * MIB);                          /* no limit here */
    printf("parent: 256 MiB %s\n", q != NULL ? "allocated" : "refused");
    free(q);
    return 0;
}
