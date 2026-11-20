/* forgot_close.c: the parent keeps the write end open; the reader never sees end of file. */
// capture: timeout=3 exit
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    int fd[2];
    if (pipe(fd) != 0) return 1;
    pid_t r = fork();
    if (r == 0) {                                /* the reader: wc counts what arrives */
        dup2(fd[0], 0);
        close(fd[0]);
        close(fd[1]);
        execlp("wc", "wc", "-c", (char *)NULL);
        _exit(127);
    }
    close(fd[0]);
    if (write(fd[1], "twelve bytes", 12) != 12) return 1;
    printf("parent: wrote 12 bytes, now waiting for wc\n");
    fflush(stdout);
    /* close(fd[1]);   <- the missing line */
    waitpid(r, NULL, 0);                         /* wc waits for end of file: forever */
    printf("parent: never printed\n");
    return 0;
}
