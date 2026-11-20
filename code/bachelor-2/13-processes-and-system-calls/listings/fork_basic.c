/* fork_basic.c: one process becomes two; each learns which one it is from fork's result. */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    int books = 10;
    pid_t me = getpid();
    pid_t r = fork();                        /* from here on, two processes run this code */
    if (r < 0) {
        perror("fork");
        return 1;
    }
    if (r == 0) {                            /* the child */
        books = 20;                          /* changes the child's copy only */
        printf("child:  fork returned 0; my parent is the caller: %s; books = %d\n",
               getppid() == me ? "yes" : "no", books);
        return 0;
    }
    pid_t done = waitpid(r, NULL, 0);        /* the parent waits for its child */
    printf("parent: fork returned my child's number: %s; books = %d\n",
           done == r ? "yes" : "no", books);
    return 0;
}
