/* cd_child.c: a child changes its working directory; its parent's does not move. */
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    char before[4096], after[4096], there[4096];
    if (!getcwd(before, sizeof before)) return 1;
    fflush(stdout);
    if (fork() == 0) {
        if (chdir("/") != 0 || !getcwd(there, sizeof there)) _exit(1);
        printf("child:  now in %s\n", there);
        fflush(stdout);                              /* _exit does not flush the buffer */
        _exit(0);
    }
    wait(NULL);
    if (!getcwd(after, sizeof after)) return 1;
    printf("parent: still where it was: %s\n", strcmp(before, after) == 0 ? "yes" : "no");
    return 0;
}
