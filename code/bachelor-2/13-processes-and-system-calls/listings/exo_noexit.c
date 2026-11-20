/* exo_noexit.c: a failed exec without _exit (exercise 6). */
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    char *commands[] = {"true", "no-such-command", "true"};
    for (int k = 0; k < 3; k++) {
        printf("running %s\n", commands[k]);
        fflush(stdout);
        if (fork() == 0) {
            char *argv[] = {commands[k], NULL};
            execvp(commands[k], argv);
            printf("exec of %s failed\n", commands[k]);   /* and then? */
        } else {
            wait(NULL);
        }
    }
    printf("done\n");
    return 0;
}
