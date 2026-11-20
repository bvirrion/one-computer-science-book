/* redirect.c: what a shell does for  echo hello > out.txt */
// capture: scratch
#include <fcntl.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    pid_t r = fork();
    if (r == 0) {
        int fd = open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        dup2(fd, 1);                              /* descriptor 1 now means out.txt */
        close(fd);                                /* the copy in 1 is enough */
        execlp("echo", "echo", "hello", (char *)NULL);
        _exit(127);
    }
    waitpid(r, NULL, 0);
    char buf[64];
    int fd = open("out.txt", O_RDONLY);
    ssize_t n = read(fd, buf, sizeof buf);
    printf("out.txt: %.*s", (int)n, buf);       /* echo never knew */
    return 0;
}
